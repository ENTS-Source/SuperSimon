
namespace SuperSimonEmulator.Commands.Concrete
{
    public class DiscoverCommand : AddressedCommand, IResponsiveCommand
    {
        public DiscoverCommand() : base(9) { } // 0000 1001

        public Command Response()
        {
            return new AcknowledgeCommand();
        }
    }
}
