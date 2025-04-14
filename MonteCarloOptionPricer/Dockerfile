# Use the .NET 9.0 preview SDK image for building the application.
FROM mcr.microsoft.com/dotnet/sdk:9.0-preview AS build
WORKDIR /app

# Copy the project file and restore dependencies.
COPY *.csproj ./
RUN dotnet restore

# Copy the rest of the source code and publish.
COPY . ./
RUN dotnet publish -c Release -o out

# Use the .NET 9.0 preview runtime image for running the application.
FROM mcr.microsoft.com/dotnet/runtime:9.0-preview
WORKDIR /app
COPY --from=build /app/out .

# Set the entry point (make sure the DLL name matches your project)
ENTRYPOINT ["dotnet", "MonteCarloOptionPricer.dll"]


