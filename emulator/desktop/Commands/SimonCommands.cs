using System;

namespace SuperSimonEmulator.Commands
{
    // `0x00` / `0` / `0000 0000`
    public class AcknowledgeCommand : Command
    {
        public AcknowledgeCommand() : base(0x00) { }
    }

    // `0x01` / `1` / `0000 0001`
    public class GameBoardInformationCommand : PayloadCommand, IResponsiveCommand
    {
        public GameBoardInformationCommand() : base(0x01) { }

        public Command Response(GamePad pad)
        {
            if (pad == null) return null;
            return new AcknowledgeCommand();
        }
    }

    // `0x02` / `2` / `0000 0010`
    public class StartGameCommand : Command
    {
        public StartGameCommand() : base(0x02) { }
    }

    // `0x03` / `3` / `0000 0011`
    public class RequestGameStateCommand : AddressedCommand, IResponsiveCommand
    {
        public RequestGameStateCommand() : base(0x03) { }

        public Command Response(GamePad pad)
        {
            if (!pad.CurrentGameComplete) return new GameNotFinishedCommand();
            return pad.CreateCompletedCommand();
        }
    }

    // `0x04` / `4` / `0000 0100`
    public class GameNotFinishedCommand : Command
    {
        public GameNotFinishedCommand() : base(0x04) { }
    }

    // `0x05` / `5` / `0000 0101`
    public class GameCompletedCommand : PayloadCommand
    {
        public GameCompletedCommand() : base(0x05) { }

        public GameCompletedCommand(byte targetAddress)
            : base(5)
        {
            TargetAddress = targetAddress;
        }

        public void AddTiming(byte buttonId, short timeToPressMs)
        {
            AppendToPayload(buttonId);
            byte[] data = BitConverter.GetBytes(timeToPressMs);
            if (BitConverter.IsLittleEndian)
                Array.Reverse(data);
            AppendToPayload(data);
        }
    }

    // `0x06` / `6` / `0000 0110`
    public class RequestJoinStateCommand : AddressedCommand, IResponsiveCommand
    {
        public RequestJoinStateCommand() : base(0x06) { }

        public Command Response(GamePad pad)
        {
            if (pad == null) return null;
            if (pad.JoinedGame) return new JoinedCommand();
            return new NotJoinedCommand();
        }
    }

    // `0x07` / `7` / `0000 0111`
    public class NotJoinedCommand : Command
    {
        public NotJoinedCommand() : base(0x07) { }
    }

    // `0x08` / `8` / `0000 1000`
    public class JoinedCommand : Command
    {
        public JoinedCommand() : base(0x08) { }
    }

    // `0x09` / `9`  / `0000 1001`
    public class DiscoverCommand : AddressedCommand, IResponsiveCommand
    {
        public DiscoverCommand() : base(0x09) { }

        public Command Response(GamePad pad)
        {
            if (pad == null) return null;
            return new AcknowledgeCommand();
        }
    }

    // `0xF0` / `240` / `1111 0000`
    public class EchoCommand : PayloadCommand, IResponsiveCommand
    {
        public EchoCommand() : base(0xF0) { }

        public Command Response(GamePad pad)
        {
            if (pad == null) return null;
            return new EchoCommand()
            {
                TargetAddress = Payload[0],
                Length = Length,
                Payload = Payload
            };
        }
    }
}
