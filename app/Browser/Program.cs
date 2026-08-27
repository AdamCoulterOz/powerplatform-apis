using Keel;
using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using PowerPlatformApis.Browser;
using PowerPlatformApis.Browser.Services;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

// specs and specs.json are served from the app's own base path
builder.Services.AddScoped(_ => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });
builder.Services.AddScoped<SpecStore>();
builder.Services.AddScoped<HashRouter>();
builder.Services.AddKeel();

await builder.Build().RunAsync();
