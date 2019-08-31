using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using SVH.FileService.Core.Models;
using SVH.FileService.Core.Services.Contracts;

namespace SVH.FileService.Host.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FilesController : ControllerBase
    {
        private readonly IFileService _fileService;

        public FilesController(IFileService fileService)
        {
            _fileService = fileService;
        }
        
        [HttpGet]
        [ProducesResponseType(typeof(ICollection<FileDto>), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        public async Task<ActionResult> Get([FromQuery] bool rescan = false)
        {
            var result = await _fileService.GetFiles(rescan);
            return Ok(result);
        }

        [HttpGet("{id}")]
        public async Task<ActionResult> Get(Guid id)
        {
            var physicalPath = await _fileService.GetFileName(id);
            return PhysicalFile(physicalPath, "video/mp4", "video.mp4");
        }
        
        [HttpGet("{id}/preview")]
        public async Task<ActionResult> GetPreview(Guid id)
        {
            var physicalPath = await _fileService.GetFileName(id);
            return PhysicalFile(physicalPath, "video/mp4", "video.mp4");
        }
        
        //todo get preview, get gif, get in format, convert in format, download torrent in path, live in format
        // POST api/values
        [HttpPost]
        public void Post([FromBody] string value)
        {
        }

        // PUT api/values/5
        [HttpPut("{id}")]
        public void Put(int id, [FromBody] string value)
        {
        }

        // DELETE api/values/5
        [HttpDelete("{id}")]
        public void Delete(int id)
        {
        }
    }
}
