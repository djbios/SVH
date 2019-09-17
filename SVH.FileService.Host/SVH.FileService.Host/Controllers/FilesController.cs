﻿using System;
using System.Collections.Generic;
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
    }
}
