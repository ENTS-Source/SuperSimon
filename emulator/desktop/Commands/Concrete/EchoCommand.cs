
namespace SuperSimonEmulator.Commands.Concrete
{
    public class EchoCommand : PayloadCommand
    {
        public EchoCommand() : base(240) { } // 1111 0000

        public EchoCommand Response()
        {
            return new EchoCommand()
            {
                TargetAddress = Payload[0],
                Length = Length,
                Payload = Payload
            };
        }
    }
}
