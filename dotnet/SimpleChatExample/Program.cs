using GraphlitClient;
using Microsoft.Extensions.Configuration;
using StrawberryShake;

public class Program
{
    public static async Task Main(string[] args)
    {
        // Build configuration
        IConfiguration configuration = new ConfigurationBuilder()
            .SetBasePath(Directory.GetCurrentDirectory())
            .AddJsonFile("appsettings.json")
            .Build();

        using var httpClient = new HttpClient();

        var client = new Graphlit(httpClient, configuration.GetSection("ClientSettings")["GRAPHLIT_ORGANIZATION_ID"], configuration.GetSection("ClientSettings")["GRAPHLIT_ENVIRONMENT_ID"], configuration.GetSection("ClientSettings")["GRAPHLIT_JWT_SECRET"], configuration.GetSection("ClientSettings")["GRAPHLIT_OWNER_ID"]);

        var id = await IngestUriAsync(client.Client, args[0], new Uri(args[1]));

        var message = await PromptConversationAsync(client.Client, args[2]);

        Console.WriteLine($"User:\n{args[2]}");
        Console.WriteLine($"Assistant:\n{message}");
    }

    private static async Task<string?> PromptConversationAsync(IGraphlitClient client, string prompt)
    {
        var result = await client.PromptConversation.ExecuteAsync(prompt, null, null);

        var response = result.Data?.PromptConversation;

        return response?.Message?.Message;
    }

    private static async Task<string?> IngestUriAsync(IGraphlitClient client, string name, Uri uri)
    {
        var result = await client.IngestUri.ExecuteAsync(name: name, uri: uri, null, true, null, null, null);

        result.EnsureNoErrors();

        var response = result.Data?.IngestUri;

        return response?.Id;
    }
}