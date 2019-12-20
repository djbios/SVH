using System;
using System.Collections.Generic;
using System.Linq;

namespace SVH.FileService.Core
{
    public static class Extensions
    {
        public static List<string> UnixifyPaths(this List<string> paths, string trimRoot = null)
        {
            Func<string, string> f;
            if (trimRoot == null)
                f = p => p.Replace('\\', '/').TrimStart('/');
            else 
                f = p => p.Replace(trimRoot, "").Replace('\\', '/').TrimStart('/'); 

            return paths.ToList().ConvertAll(p => f(p));
        }
    }
}
