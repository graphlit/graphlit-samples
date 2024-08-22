#region Using directives

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
            [Option('s', "summarization-type", Default = null, HelpText = "Summarization Type")]
            public SummarizationTypes? SummarizationType { get; set; }

            [Option('l', "llm-type", Default = LLMTypes.Anthropic, HelpText = "LLM Type")]
            public LLMTypes? LLMType { get; set; }

            [Option('p', "preparation-type", Default = PreparationTypes.Default, HelpText = "Preparation Type")]
            public PreparationTypes? PreparationType { get; set; }

            [Option('f', "output-format", Default = OutputFormats.Markdown, HelpText = "Output Format")]
            public OutputFormats? Format { get; set; }

            [Option('i', "input", Required = true, Default = null, HelpText = "File or Webpage URI, or Local File Path")]
            public string? Input { get; set; }

            [Option('o', "output-file-path", HelpText = "Output File Path")]
            public string? OutputFilePath { get; set; }
        }

        #endregion

        public static async Task Main(string[] args)
        {
            IConfiguration configuration = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json")
#if DEBUG_BUILD
                .AddJsonFile("appsettings.Development.json")
#endif
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
            (var preparationSpecification, var extractionSpecification, var workflow) = 
                await InitializeAsync(client, configuration, options.SummarizationType, options.PreparationType ?? PreparationTypes.Default, options.LLMType ?? LLMTypes.Anthropic);

            string? id = null;

            try
            {
                Console.WriteLine();

                Timer progressTimer = new Timer(_ =>
                {
                    Console.Write(".");
                }, null, TimeSpan.Zero, TimeSpan.FromSeconds(1));

                if (Uri.TryCreate(options.Input, UriKind.Absolute, out var uri))
                {
                    Console.WriteLine($"Attempting to parse content [{uri}].");

                    id = await IngestUriAsync(client, uri, workflow, sessionId);

                    if (id == null)
                        throw new InvalidOperationException($"Failed to ingest content [{uri}].");
                }
                else if (!String.IsNullOrWhiteSpace(options.Input))
                {
                    Console.WriteLine($"Attempting to parse content [{options.Input}].");

                    id = await IngestFileAsync(client, options.Input, workflow, sessionId);

                    if (id == null)
                        throw new InvalidOperationException($"Failed to ingest content [{options.Input}].");
                }
                else
                {
                    throw new InvalidOperationException("Invalid source.");
                }

                progressTimer.Dispose();

                var content = await GetContentAsync(client, id);

                if (content == null)
                    throw new InvalidOperationException($"Failed to get content [{id}].");

                if (content.State == EntityState.Errored)
                    throw new InvalidOperationException(content.Error);

                var credits = await LookupCreditsAsync(client, sessionId) ?? throw new InvalidOperationException("Failed to lookup credits.");

                Console.WriteLine();
                Console.WriteLine($"Parsed content [{content.FileName}], used {credits:F4} credits, took {content.WorkflowDuration}.");                

#if DEBUG_BUILD
                //
                // NOTE: uncomment to write out the content JSON to console
                //
                //Console.WriteLine(JsonConvert.SerializeObject(content, Formatting.Indented));
#endif

                if (!String.IsNullOrEmpty(options.OutputFilePath))
                {
                    if (options.Format == OutputFormats.Markdown)
                    {
                        await File.WriteAllTextAsync(options.OutputFilePath, content.Markdown);

                        Console.WriteLine($"Wrote Markdown file [{options.OutputFilePath}].");
                    }
                    else if (options.Format == OutputFormats.Json)
                    {
                        var jsonUri = content.TranscriptUri ?? content.TextUri;

                        if (jsonUri != null)
                        {
                            string json = await httpClient.GetStringAsync(jsonUri);

                            await File.WriteAllTextAsync(options.OutputFilePath, json);

                            Console.WriteLine($"Wrote JSON file [{options.OutputFilePath}].");
                        }
                    }
                }
                else
                {
                    string? text = (content.Type == ContentTypes.File && content.FileType == FileTypes.Image) ? content.Image?.Description : content.Markdown;

                    Console.WriteLine();

                    if (!String.IsNullOrEmpty(text))
                    {
                        Console.WriteLine("--------------------------------------------------------------------------------");
                        Console.WriteLine();
                        Console.WriteLine(text);
                        Console.WriteLine();
                        Console.WriteLine("--------------------------------------------------------------------------------");
                    }
                    else
                    {
                        Console.WriteLine("No text was parsed.");
                    }

                    if (options.SummarizationType != null)
                    {
                        Console.WriteLine();

                        switch (options.SummarizationType)
                        {
                            case SummarizationTypes.Summary:
                                if (!String.IsNullOrWhiteSpace(content.Summary))
                                {
                                    Console.WriteLine($"Summary:");
                                    Console.WriteLine();
                                    Console.WriteLine(content.Summary);
                                }
                                break;
                            case SummarizationTypes.Posts:
                                if (content.Posts != null)
                                {
                                    Console.WriteLine($"Social Media Posts:");
                                    Console.WriteLine();
                                    Console.WriteLine(String.Join('\n', content.Posts));
                                }
                                break;
                            case SummarizationTypes.Bullets:
                                if (content.Bullets != null)
                                {
                                    Console.WriteLine($"Bullets:");
                                    Console.WriteLine();
                                    Console.WriteLine(String.Join('\n', content.Bullets));
                                }
                                break;
                            case SummarizationTypes.Headlines:
                                if (content.Headlines != null)
                                {
                                    Console.WriteLine($"Headlines:");
                                    Console.WriteLine();
                                    Console.WriteLine(String.Join('\n', content.Headlines));
                                }
                                break;
                            case SummarizationTypes.Questions:
                                if (content.Questions != null)
                                {
                                    Console.WriteLine($"Questions:");
                                    Console.WriteLine();
                                    Console.WriteLine(String.Join('\n', content.Questions));
                                }
                                break;
                            case SummarizationTypes.Keywords:
                                if (content.Keywords != null)
                                {
                                    Console.WriteLine($"Keywords:");
                                    Console.WriteLine();
                                    Console.WriteLine(String.Join(',', content.Keywords));
                                }
                                break;
                            case SummarizationTypes.Chapters:
                                if (content.Chapters != null)
                                {
                                    Console.WriteLine($"Chapters:");
                                    Console.WriteLine();
                                    Console.WriteLine(String.Join('\n', content.Chapters));
                                }
                                break;
                        }
                    }
                }
            }
            finally
            {
                await CleanAsync(client, preparationSpecification, extractionSpecification, workflow, id);
            }
        }

        #region Helper methods

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

        private static async Task<(EntityReferenceInput? PreparationSpecification, EntityReferenceInput ExtractionSpecification, EntityReferenceInput Workflow)> 
            InitializeAsync(IGraphlitClient client, IConfiguration configuration, SummarizationTypes? summarizationType, PreparationTypes preparationType, LLMTypes llmType)
        {
            Console.WriteLine("Initializing.");

            var preparationSpecification = preparationType == PreparationTypes.LLM ? await CreatePreparationSpecificationAsync(client, configuration, llmType) : null;
            var extractionSpecification = await CreateExtractionSpecificationAsync(client, configuration, llmType);

            var wid = await CreateWorkflowAsync(client, configuration, summarizationType, preparationSpecification, extractionSpecification) ?? throw new InvalidOperationException("Failed to create workflow.");

            Console.WriteLine($"Created workflow [{wid}].");

            var workflow = new EntityReferenceInput { Id = wid };

            return (preparationSpecification, extractionSpecification, workflow);
        }

        private static async Task<EntityReferenceInput> CreatePreparationSpecificationAsync(IGraphlitClient client, IConfiguration configuration, LLMTypes llmType)
        {
            var sid = await CreateSpecificationAsync(client, configuration, SpecificationTypes.Preparation, llmType) ?? throw new InvalidOperationException("Failed to create preparation specification.");

            Console.WriteLine($"Created preparation specification [{sid}].");

            return new EntityReferenceInput { Id = sid };
        }

        private static async Task<EntityReferenceInput> CreateExtractionSpecificationAsync(IGraphlitClient client, IConfiguration configuration, LLMTypes llmType)
        {
            var sid = await CreateSpecificationAsync(client, configuration, SpecificationTypes.Extraction, llmType) ?? throw new InvalidOperationException("Failed to create extraction specification.");

            Console.WriteLine($"Created extraction specification [{sid}].");

            return new EntityReferenceInput { Id = sid };
        }

        private static async Task<string?> CreateSpecificationAsync(IGraphlitClient client, IConfiguration configuration, SpecificationTypes specificationType, LLMTypes llmType)
        {
            SpecificationInput specification;

            switch (llmType)
            {
                case LLMTypes.OpenAI:
                    {
                        string? key = configuration.GetSection("ModelSettings")["OPENAI_API_KEY"];
                        string? modelName = configuration.GetSection("ModelSettings")["OPENAI_MODEL"];

                        specification = new SpecificationInput
                        {
                            Name = $"{specificationType} Specification",
                            Type = specificationType,
                            ServiceType = ModelServiceTypes.OpenAi,
                            OpenAI = new OpenAIModelPropertiesInput
                            {
                                Model = String.IsNullOrWhiteSpace(key) ? OpenAIModels.Gpt4o128k20240806 : OpenAIModels.Custom,
                                ModelName = String.IsNullOrWhiteSpace(key) ? null : modelName,
                                Key = key
                            }
                        };
                    }
                    break;
                case LLMTypes.Anthropic:
                    {
                        string? key = configuration.GetSection("ModelSettings")["ANTHROPIC_API_KEY"];
                        string? modelName = configuration.GetSection("ModelSettings")["ANTHROPIC_MODEL"];

                        specification = new SpecificationInput
                        {
                            Name = $"{specificationType} Specification",
                            Type = specificationType,
                            ServiceType = ModelServiceTypes.Anthropic,
                            Anthropic = new AnthropicModelPropertiesInput
                            {
                                Model = String.IsNullOrWhiteSpace(key) ? AnthropicModels.Claude35Sonnet : AnthropicModels.Custom,
                                ModelName = String.IsNullOrWhiteSpace(key) ? null : modelName,
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

        private static async Task<string?> CreateWorkflowAsync(IGraphlitClient client, IConfiguration configuration, SummarizationTypes? summarizationType,
            EntityReferenceInput? preparationSpecification, EntityReferenceInput extractionSpecification)
        {
            var workflow = new WorkflowInput
            {
                Name = "Workflow",
                Preparation = new PreparationWorkflowStageInput
                {
                    Summarizations = summarizationType != null ? new List<SummarizationStrategyInput>
                    {
                        new SummarizationStrategyInput { Type = summarizationType.Value }
                    } : null,
                    Jobs = preparationSpecification != null ? new List<PreparationWorkflowJobInput>
                    {
                          new PreparationWorkflowJobInput
                          {
                               Connector = new FilePreparationConnectorInput { Type = FilePreparationServiceTypes.ModelDocument, ModelDocument = new ModelDocumentPreparationInputProperties { Specification = preparationSpecification } }
                          }
                    } : null
                },
                Extraction = new ExtractionWorkflowStageInput
                {
                    Jobs = new List<ExtractionWorkflowJobInput>
                    {
                          new ExtractionWorkflowJobInput
                          {
                               Connector = new EntityExtractionConnectorInput { Type = EntityExtractionServiceTypes.ModelImage, ModelImage = new ModelImageExtractionPropertiesInput { Specification = extractionSpecification } }
                          }
                    }
                },
            };

            var result = await client.CreateWorkflow.ExecuteAsync(workflow);

            result.EnsureNoErrors();

            var response = result.Data?.CreateWorkflow;

            return response?.Id;
        }

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

        private static async Task<decimal?> LookupCreditsAsync(IGraphlitClient client, string sessionId)
        {
            var result = await client.LookupCredits.ExecuteAsync(sessionId);

            result.EnsureNoErrors();

            var response = result.Data?.LookupCredits;

            return response?.Credits;
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

        private static async Task CleanAsync(IGraphlitClient client, EntityReferenceInput? preparationSpecification, EntityReferenceInput? extractionSpecification, EntityReferenceInput? workflow, string? id)
        {
            if (workflow != null)
                await DeleteWorkflowAsync(client, workflow.Id);

            if (preparationSpecification != null)
                await DeleteSpecificationAsync(client, preparationSpecification.Id);

            if (extractionSpecification != null)
                await DeleteSpecificationAsync(client, extractionSpecification.Id);

            if (!String.IsNullOrEmpty(id))
                await DeleteContentAsync(client, id);
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

        #endregion
    }
}
