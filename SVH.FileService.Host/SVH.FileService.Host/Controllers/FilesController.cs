﻿using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using SVH.FileService.Core.Models;
using SVH.FileService.Core.Services.Contracts;

namespace SVH.FileService.Host.Controllers
{
    [Route("api/files")]
    [ApiController]
    public class FilesController : ControllerBase
    {
        private readonly IFileService _fileService;
        private readonly IStorage _storage;

        public FilesController(IFileService fileService, IStorage storage)
        {
            _fileService = fileService;
            _storage = storage;
        }
        
        [HttpGet()]
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
            var relativePath = await _fileService.GetFileName(id);
            return Redirect($"storage?path={relativePath}");
        }

        [HttpGet("storage/")]
        public async Task<ActionResult> GetFs(string path)
        {
            var fullPath = await _storage.GetFullFilePath(path);
            return PhysicalFile(fullPath, "application/octet-stream", Path.GetFileName(fullPath));
        }
    }
}
