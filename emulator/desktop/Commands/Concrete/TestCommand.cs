using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SuperSimonEmulator.Commands.Concrete
{
    public class TestCommand : PayloadCommand
    {
        public TestCommand() : base(0x5) { }
    }
}
