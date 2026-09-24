using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RecordsApi.Data;
using RecordsApi.Models;

namespace RecordsApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class RecordsController : ControllerBase
{
    private readonly AppDbContext _db;

    public RecordsController(AppDbContext db)
    {
        _db = db;
    }

    // GET /api/records
    [HttpGet]
    public async Task<ActionResult<IEnumerable<Record>>> GetAll()
    {
        var records = await _db.Records.OrderByDescending(r => r.CreatedAt).ToListAsync();
        return Ok(records);
    }

    // GET /api/records/5
    [HttpGet("{id:int}")]
    public async Task<ActionResult<Record>> GetById(int id)
    {
        var record = await _db.Records.FindAsync(id);
        if (record is null) return NotFound();
        return Ok(record);
    }

    // POST /api/records
    [HttpPost]
    public async Task<ActionResult<Record>> Create([FromBody] Record input)
    {
        var record = new Record
        {
            Title = input.Title,
            Description = input.Description,
            CreatedAt = DateTime.UtcNow,
        };

        _db.Records.Add(record);
        await _db.SaveChangesAsync();

        return CreatedAtAction(nameof(GetById), new { id = record.Id }, record);
    }

    // PUT /api/records/5
    [HttpPut("{id:int}")]
    public async Task<IActionResult> Update(int id, [FromBody] Record input)
    {
        var record = await _db.Records.FindAsync(id);
        if (record is null) return NotFound();

        record.Title = input.Title;
        record.Description = input.Description;
        await _db.SaveChangesAsync();

        return NoContent();
    }

    // DELETE /api/records/5
    [HttpDelete("{id:int}")]
    public async Task<IActionResult> Delete(int id)
    {
        var record = await _db.Records.FindAsync(id);
        if (record is null) return NotFound();

        _db.Records.Remove(record);
        await _db.SaveChangesAsync();

        return NoContent();
    }
}
