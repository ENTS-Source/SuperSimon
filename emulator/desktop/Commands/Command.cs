
namespace SuperSimonEmulator.Commands
{
    /// <summary>
    /// Represents a command within the Super Simon protocol
    /// </summary>
    public abstract class Command
    {
        /// <summary>
        /// Gets the ID of this command
        /// </summary>
        public byte CommandId { get; private set; }

        /// <summary>
        /// Gets whether or not this command is expecting more bytes
        /// </summary>
        public virtual bool ExpectingMoreBytes { get { return !HasConsumedCommand; } }

        /// <summary>
        /// Gets whether or not this command has consumed the command ID byte
        /// </summary>
        protected bool HasConsumedCommand { get; private set; }

        /// <summary>
        /// Creates a new command
        /// </summary>
        /// <param name="commandId">The ID of the command</param>
        protected Command(byte commandId)
        {
            CommandId = commandId;
        }

        /// <summary>
        /// Consumes a byte for this command
        /// </summary>
        /// <param name="b">The byte to consume</param>
        /// <returns>The result of the consume attempt</returns>
        public virtual ConsumeResult ConsumeByte(byte b)
        {
            if (!HasConsumedCommand)
            {
                if (b != CommandId)
                    return ConsumeResult.InvalidByte;
                HasConsumedCommand = true;
                return ConsumeResult.Consumed;
            }
            return ConsumeResult.NotConsumed;
        }
    }

    /// <summary>
    /// Represents the different consume results that are possible
    /// </summary>
    public enum ConsumeResult
    {
        /// <summary>
        /// The byte given was consumed
        /// </summary>
        Consumed,

        /// <summary>
        /// The byte given is not applicable for the sequence
        /// </summary>
        InvalidByte,

        /// <summary>
        /// The byte given was not consumed because the command has consumed all applicable bytes
        /// </summary>
        NotConsumed
    }
}
