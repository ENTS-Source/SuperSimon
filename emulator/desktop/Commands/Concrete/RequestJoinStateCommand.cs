
namespace SuperSimonEmulator.Commands.Concrete
{
    public class RequestJoinStateCommand : AddressedCommand, IResponsiveCommand
    {
        public RequestJoinStateCommand() : base(6) { } // 0000 0110

        public Command Response(GamePad pad)
        {
            if (pad.JoinedGame) return new JoinedCommand();
            return new NotJoinedCommand();
        }
    }
}
