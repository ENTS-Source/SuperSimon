using System;
using System.Collections.Generic;

namespace SuperSimonEmulator.Commands
{
    /// <summary>
    /// Represents a command with a payload
    /// </summary>
    public abstract class PayloadCommand : AddressedCommand
    {
        private List<byte> _payload = new List<byte>();
        private List<byte> _lengthBytes = new List<byte>();

        public override bool ExpectingMoreBytes { get { return base.ExpectingMoreBytes || !IsComplete; } }

        /// <summary>
        /// Gets the length of the payload. Returns null if not yet determined
        /// </summary>
        public int? Length { get; protected set; }

        /// <summary>
        /// Gets the known payload for this command. Never returns null, although the resulting array size
        /// may not match the length defined. This command is considered complete when the payload length
        /// matches the defined length. If no length has been determined then this will return a 0-length
        /// array.
        /// </summary>
        public byte[] Payload
        {
            get { return _payload.ToArray(); }
            protected set { _payload = new List<byte>(value); }
        }

        /// <summary>
        /// Gets whether or not the payload has been fully read
        /// </summary>
        public bool IsComplete { get { return Length.HasValue && Length == Payload.Length; } }

        protected PayloadCommand(byte commandId) : base(commandId) { }

        public override ConsumeResult ConsumeByte(byte b)
        {
            var baseResult = base.ConsumeByte(b);
            if (baseResult == ConsumeResult.NotConsumed)
            {
                bool used = false;
                if (_lengthBytes.Count != 4)
                {
                    _lengthBytes.Add(b);
                    used = true;
                }
                if (_lengthBytes.Count == 4 && Length == null)
                    ConvertLength();
                if (Length != null && !used)
                {
                    if (_payload.Count != Length)
                    {
                        _payload.Add(b);
                        used = true;
                    }
                }
                return used ? ConsumeResult.Consumed : ConsumeResult.NotConsumed;
            }
            return baseResult;
        }

        /// <summary>
        /// Adds a series of bytes to the payload
        /// </summary>
        /// <param name="b">The bytes to add</param>
        protected void AppendToPayload(params byte[] b)
        {
            if (Length == null) Length = 0;
            _payload.AddRange(b);
            Length += b.Length;
        }

        private void ConvertLength()
        {
            byte[] raw = _lengthBytes.ToArray();

            // If the system architecture is little endian then we need to reverse the bytes
            if (BitConverter.IsLittleEndian)
                Array.Reverse(raw);

            Length = BitConverter.ToInt32(raw, 0);
        }
    }
}
