﻿#region Using directives

using CommandLine;
using GraphlitClient;
using HeyRed.Mime;
using Microsoft.Extensions.Configuration;
using StrawberryShake;

#endregion

namespace GraphlitIngest
{
    public enum PreparationTypes
    {
        Default,
        LLM
    }

    public enum OutputFormats
    {
        Markdown,
        Json
    }

    public enum LLMTypes
    {
        Anthropic,
        OpenAI
    }

    public class Program
    {
        #region Options

        [Verb("parse", HelpText = "Parse content.")]
        private class ParseOptions
        {
            [Option('l', "llm-type", Default = LLMTypes.Anthropic, HelpText = "LLM Type")]
            public LLMTypes? LLMType { get; set; }

            [Option('p', "preparation-type", Default = PreparationTypes.Default, HelpText = "Preparation Type")]
            public PreparationTypes? PreparationType { get; set; }

            [Option('f', "output-format", Default = OutputFormats.Markdown, HelpText = "Output Format")]
            public OutputFormats? Format { get; set; }

            [Option('i', "file-path", Default = null, HelpText = "File Path")]
            public string? FilePath { get; set; }

            [Option('u', "uri", Default = null, HelpText = "File or Webpage URI")]
            public string? Uri { get; set; }

            [Option('o', "output-file-path", HelpText = "Output File Path")]
            public string? OutputFilePath { get; set; }
        }

        #endregion

        public static async Task Main(string[] args)
        {
            IConfiguration configuration = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json")
                .Build();

            using var httpClient = new HttpClient();

            httpClient.Timeout = TimeSpan.FromMinutes(30);

            var sessionId = Guid.NewGuid().ToString(); // NOTE: treat each run as a separate user session

            try
            {
                var client = CreateClient(configuration, httpClient, sessionId) ?? throw new InvalidOperationException("Failed to create Graphlit client.");

                Parser.Default.ParseArguments(args, new Type[]
                {
                    typeof(ParseOptions)
                })
                .WithParsed<ParseOptions>(options =>
                {
                    try
                    {
                        if (String.IsNullOrWhiteSpace(options.FilePath) && String.IsNullOrWhiteSpace(options.Uri))
                            throw new InvalidOperationException("ERROR: Source file path or URI required.");

                        ParseContentAsync(client, configuration, httpClient, options, sessionId).Wait();
                    }
                    catch (Exception e)
                    {
                        HandleCommandException(e);
                    }
                })
                .WithNotParsed(HandleCommandError);
            }
            catch (Exception e)
            {
                HandleCommandException(e);
            }
        }

        private static async Task ParseContentAsync(IGraphlitClient client, IConfiguration configuration, HttpClient httpClient, ParseOptions options, string sessionId)
        {
            (var specification, var workflow) = options.PreparationType == PreparationTypes.LLM ? await InitializeAsync(client, configuration, options.LLMType ?? LLMTypes.OpenAI) : default;

            string? id = null;

            try
            {
                if (!String.IsNullOrWhiteSpace(options.FilePath))
                {
                    Console.WriteLine($"Attempting to parse content [{options.FilePath}].");

                    id = await IngestFileAsync(client, options.FilePath, workflow, sessionId);

                    if (id == null)
                        throw new InvalidOperationException($"Failed to ingest content [{options.FilePath}].");
                }
                else if (!String.IsNullOrWhiteSpace(options.Uri))
                {
                    Console.WriteLine($"Attempting to parse content [{options.Uri}].");

                    id = await IngestUriAsync(client, new Uri(options.Uri), workflow, sessionId);

                    if (id == null)
                        throw new InvalidOperationException($"Failed to ingest content [{options.Uri}].");
                }
                else
                {
                    throw new InvalidOperationException("Invalid source.");
                }

                var content = await GetContentAsync(client, id);

                if (content == null)
                    throw new InvalidOperationException($"Failed to get content [{id}].");

                var credits = await LookupCreditsAsync(client, sessionId) ?? throw new InvalidOperationException("Failed to lookup credits.");

                Console.WriteLine();
                Console.WriteLine($"Parsed content [{content.FileName}], used {credits:F4} credits, took {content.WorkflowDuration}.");
                Console.WriteLine();

                if (!String.IsNullOrEmpty(options.OutputFilePath))
                {
                    if (options.Format == OutputFormats.Markdown)
                    {
                        await File.WriteAllTextAsync(options.OutputFilePath, content.Markdown);

                        Console.WriteLine($"Wrote Markdown file [{options.OutputFilePath}].");
                    }
                    else if (options.Format == OutputFormats.Json)
                    {
                        string json = await httpClient.GetStringAsync(content.TextUri);

                        await File.WriteAllTextAsync(options.OutputFilePath, json);

                        Console.WriteLine($"Wrote JSON file [{options.OutputFilePath}].");
                    }
                }
                else
                {
                    Console.WriteLine(content.Markdown);
                }
            }
            finally
            {
                await CleanAsync(client, specification, workflow, id);
            }
        }

        private static async Task<decimal?> LookupCreditsAsync(IGraphlitClient client, string sessionId)
        {
            var result = await client.LookupCredits.ExecuteAsync(sessionId);

            result.EnsureNoErrors();

            var response = result.Data?.LookupCredits;

            return response?.Credits;
        }

        #region Helper methods

        private static async Task<string?> IngestUriAsync(IGraphlitClient client, Uri uri, EntityReferenceInput? workflow, string sessionId)
        {
            var result = await client.IngestUri.ExecuteAsync(null, uri, null, true, workflow, null, sessionId);

            result.EnsureNoErrors();

            var response = result.Data?.IngestUri;

            return response?.Id;
        }

        private static async Task<string?> IngestFileAsync(IGraphlitClient client, string filePath, EntityReferenceInput? workflow, string sessionId)
        {
            string fileName = Path.GetFileName(filePath);
            string name = Path.GetFileNameWithoutExtension(fileName);

            var data = await File.ReadAllBytesAsync(filePath);
            string mimeType = MimeTypesMap.GetMimeType(fileName);

            var result = await client.IngestEncodedFile.ExecuteAsync(name, Convert.ToBase64String(data), mimeType, null, true, null, workflow, sessionId);

            result.EnsureNoErrors();

            var response = result.Data?.IngestEncodedFile;

            return response?.Id;
        }

        private static async Task<IGetContent_Content?> GetContentAsync(IGraphlitClient client, string id)
        {
            var result = await client.GetContent.ExecuteAsync(id);

            result.EnsureNoErrors();

            var response = result.Data?.Content;

            return response;
        }

        private static async Task DeleteSpecificationAsync(IGraphlitClient client, string id)
        {
            var result = await client.DeleteSpecification.ExecuteAsync(id);

            result.EnsureNoErrors();
        }

        private static async Task DeleteWorkflowAsync(IGraphlitClient client, string id)
        {
            var result = await client.DeleteWorkflow.ExecuteAsync(id);

            result.EnsureNoErrors();
        }

        private static async Task DeleteContentAsync(IGraphlitClient client, string id)
        {
            var result = await client.DeleteContent.ExecuteAsync(id);

            result.EnsureNoErrors();
        }

        private static IGraphlitClient? CreateClient(IConfiguration configuration, HttpClient httpClient, string sessionId)
        {
            string? organizationId = configuration.GetSection("ClientSettings")["GRAPHLIT_ORGANIZATION_ID"];
            string? environmentId = configuration.GetSection("ClientSettings")["GRAPHLIT_ENVIRONMENT_ID"];
            string? jwtSecret = configuration.GetSection("ClientSettings")["GRAPHLIT_JWT_SECRET"];

            if (String.IsNullOrWhiteSpace(organizationId))
                throw new InvalidOperationException("Invalid Graphlit organization ID.");

            if (String.IsNullOrWhiteSpace(environmentId))
                throw new InvalidOperationException("Invalid Graphlit environment ID.");

            if (String.IsNullOrWhiteSpace(jwtSecret))
                throw new InvalidOperationException("Invalid Graphlit JWT secret.");

            var client = new Graphlit(httpClient, organizationId, environmentId, jwtSecret, sessionId);

            return client?.Client;
        }

        private static void HandleCommandError(IEnumerable<Error> errors)
        {
            foreach (var error in errors)
                Console.WriteLine($"Recognized command error [{error}].");
        }

        private static void HandleCommandException(Exception e)
        {
            Console.WriteLine();

            Console.Write("ERROR: ");

            if (e is AggregateException ex)
            {
                foreach (var ie in ex.InnerExceptions)
                    Console.WriteLine(ie.Message);
            }
            else
            {
                Console.WriteLine(e.Message);
            }

#if DEBUG_BUILD
            if (e.InnerException != null)
            {
                Console.WriteLine(e.InnerException.Message);

                if (e.InnerException.InnerException != null)
                    Console.WriteLine(e.InnerException.InnerException.Message);
            }
#endif
        }

        private static async Task<(EntityReferenceInput Specification, EntityReferenceInput Workflow)> InitializeAsync(IGraphlitClient client, IConfiguration configuration, LLMTypes llmType)
        {
            Console.WriteLine("Initializing.");

            var sid = await CreateSpecificationAsync(client, configuration, llmType) ?? throw new InvalidOperationException("Failed to create preparation specification.");

            Console.WriteLine($"Created specification [{sid}].");

            var specification = new EntityReferenceInput { Id = sid };

            var wid = await CreateWorkflowAsync(client, configuration, specification) ?? throw new InvalidOperationException("Failed to create workflow.");

            Console.WriteLine($"Created workflow [{wid}].");

            var workflow = new EntityReferenceInput { Id = wid };

            return (specification, workflow);
        }

        private static async Task CleanAsync(IGraphlitClient client, EntityReferenceInput? specification, EntityReferenceInput? workflow, string? id)
        {
            if (workflow != null)
                await DeleteWorkflowAsync(client, workflow.Id);

            if (specification != null)
                await DeleteSpecificationAsync(client, specification.Id);

            if (!String.IsNullOrEmpty(id))
                await DeleteContentAsync(client, id);
        }

        private static async Task<string?> CreateSpecificationAsync(IGraphlitClient client, IConfiguration configuration, LLMTypes llmType)
        {
            SpecificationInput specification;

            switch (llmType)
            {
                case LLMTypes.OpenAI:
                    {
                        string? key = configuration.GetSection("ModelSettings")["OPENAI_API_KEY"];

                        specification = new SpecificationInput
                        {
                            Name = "Preparation Specification",
                            Type = SpecificationTypes.Preparation,
                            ServiceType = ModelServiceTypes.OpenAi,
                            OpenAI = new OpenAIModelPropertiesInput
                            {
                                Model = String.IsNullOrWhiteSpace(key) ? OpenAIModels.Gpt4o128k20240806 : OpenAIModels.Custom,
                                Key = key
                            }
                        };
                    }
                    break;
                case LLMTypes.Anthropic:
                    {
                        string? key = configuration.GetSection("ModelSettings")["ANTHROPIC_API_KEY"];

                        specification = new SpecificationInput
                        {
                            Name = "Preparation Specification",
                            Type = SpecificationTypes.Preparation,
                            ServiceType = ModelServiceTypes.Anthropic,
                            Anthropic = new AnthropicModelPropertiesInput
                            {
                                Model = String.IsNullOrWhiteSpace(key) ? AnthropicModels.Claude35Sonnet : AnthropicModels.Custom,
                                Key = key
                            }
                        };
                    }
                    break;
                default:
                    throw new InvalidOperationException($"Unsupported LLM type [{llmType}].");
            }

            var result = await client.CreateSpecification.ExecuteAsync(specification);

            result.EnsureNoErrors();

            var response = result.Data?.CreateSpecification;

            return response?.Id;
        }

        private static async Task<string?> CreateWorkflowAsync(IGraphlitClient client, IConfiguration configuration, EntityReferenceInput specification)
        {
            var workflow = new WorkflowInput
            {
                Name = "Preparation Workflow",
                Preparation = new PreparationWorkflowStageInput
                {
                    Jobs = new List<PreparationWorkflowJobInput>
                    {
                          new PreparationWorkflowJobInput
                          {
                               Connector = new FilePreparationConnectorInput { Type = FilePreparationServiceTypes.ModelDocument, ModelDocument = new ModelDocumentPreparationInputProperties { Specification = specification } }
                          }
                    }
                }
            };

            var result = await client.CreateWorkflow.ExecuteAsync(workflow);

            result.EnsureNoErrors();

            var response = result.Data?.CreateWorkflow;

            return response?.Id;
        }

        #endregion
    }
}
