
namespace SuperSimonEmulator.Commands.Concrete
{
    public class RequestJoinStateCommand : AddressedCommand, IResponsiveCommand
    {
        public RequestJoinStateCommand() : base(6) { } // 0000 0110

        public Command Response()
        {
            return new NotJoinedCommand(); // TODO: Actual response - game pad?
        }
    }
}
