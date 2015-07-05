
namespace SuperSimonEmulator.Commands.Concrete
{
    public class StartGameCommand : AddressedCommand
    {
        public StartGameCommand() : base(2) { } // 0000 0010
    }
}
