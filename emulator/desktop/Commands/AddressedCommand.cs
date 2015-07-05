
namespace SuperSimonEmulator.Commands
{
    /// <summary>
    /// Represents a command that is addressed to a specific client
    /// </summary>
    public abstract class AddressedCommand : Command
    {
        /// <summary>
        /// Gets the address that has been targetted. Null if not yet targetted.
        /// </summary>
        public byte? TargetAddress { get; private set; }

        public override bool ExpectingMoreBytes { get { return base.ExpectingMoreBytes || TargetAddress == null; } }

        protected AddressedCommand(byte commandId) : base(commandId) { }

        public override ConsumeResult ConsumeByte(byte b)
        {
            var baseResult = base.ConsumeByte(b);
            if (baseResult == ConsumeResult.NotConsumed)
            {
                if (TargetAddress.HasValue)
                    return ConsumeResult.NotConsumed;
                TargetAddress = b;
                return ConsumeResult.Consumed;
            }
            return baseResult;
        }
    }
}
