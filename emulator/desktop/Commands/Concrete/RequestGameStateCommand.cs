
namespace SuperSimonEmulator.Commands.Concrete
{
    public class RequestGameStateCommand : AddressedCommand, IResponsiveCommand
    {
        public RequestGameStateCommand() : base(3) { } // 0000 0011

        public Command Response()
        {
            return new GameNotFinishedCommand(); // TODO: Actual response - game pad?
        }
    }
}
