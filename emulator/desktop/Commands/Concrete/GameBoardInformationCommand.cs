
namespace SuperSimonEmulator.Commands.Concrete
{
    public class GameBoardInformationCommand : PayloadCommand, IResponsiveCommand
    {
        public GameBoardInformationCommand() : base(1) { } // 0000 0001

        public Command Response()
        {
            return new AcknowledgeCommand();
        }
    }
}
