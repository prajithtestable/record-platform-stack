using Microsoft.EntityFrameworkCore;
using RecordsApi.Data;

var builder = WebApplication.CreateBuilder(args);

// Controllers (Model + Controller layer of the MVC pattern; React is the View layer, served separately)
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// EF Core + SQL Server
var connectionString = builder.Configuration.GetConnectionString("Default")
    ?? "Server=sql-server,1433;Database=RecordsDb;User Id=sa;Password=Your_password123;TrustServerCertificate=True;";
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(connectionString));

// Allow the React dev server (Vite, default port 5173) to call the API in local development
builder.Services.AddCors(options =>
{
    options.AddPolicy("ClientApp", policy =>
        policy.WithOrigins("http://localhost:5173")
              .AllowAnyHeader()
              .AllowAnyMethod());
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors("ClientApp");
app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

// Ensure the database/schema exists on startup (no separate EF migration step required for this reference app)
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.EnsureCreated();
}

app.Run();
