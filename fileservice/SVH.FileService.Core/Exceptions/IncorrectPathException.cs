using System;

namespace SVH.FileService.Core.Exceptions
{
    public class IncorrectPathException : Exception
    {
        public IncorrectPathException(string message) : base(message)
        {
            
        }
    }
}
