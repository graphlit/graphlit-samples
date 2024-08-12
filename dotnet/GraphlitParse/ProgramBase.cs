#region Using directives

using CommandLine;
using GraphlitClient;
using HeyRed.Mime;
using Microsoft.Extensions.Configuration;
using StrawberryShake;

#endregion

namespace GraphlitCLI
{
    public enum OutputFormats
    {
        Markdown,
        Json
    }

    public abstract class ProgramBase
    {
        protected static async Task<string?> IngestUriAsync(IGraphlitClient client, Uri uri, EntityReferenceInput workflow, string sessionId)
        {
            var result = await client.IngestUri.ExecuteAsync(null, uri, null, true, workflow, null, sessionId);

            result.EnsureNoErrors();

            var response = result.Data?.IngestUri;

            return response?.Id;
        }

        protected static async Task<string?> IngestFileAsync(IGraphlitClient client, string filePath, EntityReferenceInput workflow, string sessionId)
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

        protected static async Task<IGetContent_Content?> GetContentAsync(IGraphlitClient client, string id)
        {
            var result = await client.GetContent.ExecuteAsync(id);

            result.EnsureNoErrors();

            var response = result.Data?.Content;

            return response;
        }

        protected static async Task DeleteSpecificationAsync(IGraphlitClient client, string id)
        {
            var result = await client.DeleteSpecification.ExecuteAsync(id);

            result.EnsureNoErrors();
        }

        protected static async Task DeleteWorkflowAsync(IGraphlitClient client, string id)
        {
            var result = await client.DeleteWorkflow.ExecuteAsync(id);

            result.EnsureNoErrors();
        }

        protected static async Task DeleteContentAsync(IGraphlitClient client, string id)
        {
            var result = await client.DeleteContent.ExecuteAsync(id);

            result.EnsureNoErrors();
        }

        protected static IGraphlitClient? CreateClient(IConfiguration configuration, HttpClient httpClient, string sessionId)
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

        protected static void HandleCommandError(IEnumerable<Error> errors)
        {
            foreach (var error in errors)
                Console.WriteLine($"Recognized command error [{error}].");
        }

        protected static void HandleCommandException(Exception e)
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
    }
}
