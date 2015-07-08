using SuperSimonEmulator.Commands;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO.Ports;
using System.Linq;
using System.Windows.Forms;

namespace SuperSimonEmulator
{
    public partial class Master : Form
    {
        private delegate void delVoidIntBool(int i, bool b);
        private delegate void delVoidCommand(Command cmd);

        private byte[] _magicSequence = { 0xDE, 0xAD, 0xBE, 0xEF };
        private int _magicSequenceIndex = 0;

        private List<GamePad> _gamePads = new List<GamePad>();
        private Command _currentCommand;

        public Master()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            cbPort.DataSource = SerialPort.GetPortNames();
            gbNewPad.Enabled = false;
            gpCommunication.Text = "Communication (Disconnected)";
        }

        private void spTeensy_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            while (spTeensy.BytesToRead > 0)
            {
                byte b = (byte)spTeensy.ReadByte();
                Invoke(new delVoidIntBool(AppendByteToSerialLog), b, true); // true = inbound

                if (_currentCommand == null)
                {
                    if(_magicSequenceIndex < _magicSequence.Length)
                    {
                        if(b != _magicSequence[_magicSequenceIndex])
                            continue; // Ignore byte: Unexpected
                        _magicSequenceIndex++;
                        continue; // Don't handle the byte
                    }
                    Console.WriteLine("Magic value read successfully");
                    _currentCommand = CommandRegistry.FindCommand(b);
                    if (_currentCommand == null)
                    {
                        Console.WriteLine("Failed to find command for ID: " + b + ", ignoring byte.");
                        continue;
                    }
                }

                var result = _currentCommand.ConsumeByte(b);
                if (result == ConsumeResult.InvalidByte)
                    Console.WriteLine("Command " + _currentCommand.CommandId + " did not accept byte: " + b + ", ignoring byte.");
                else if (result == ConsumeResult.NotConsumed)
                    Console.WriteLine("Command " + _currentCommand.CommandId + " did not consume byte: " + b + ", ignoring byte.");

                if (!_currentCommand.ExpectingMoreBytes)
                {
                    Invoke(new delVoidCommand(HandleCommand), _currentCommand);
                    _currentCommand = null;
                    _magicSequenceIndex = 0;
                }
            }
        }

        private void AppendByteToSerialLog(int b, bool inbound)
        {
            (inbound ? tbComLogIn : tbComLogOut).AppendText("[" + b + "]");
        }

        private void HandleCommand(Command command)
        {
            string address = command is AddressedCommand ? ((AddressedCommand)command).TargetAddress.ToString() : "<not addressed>";
            string payloadInfo = command is PayloadCommand ? "(Length=" + ((PayloadCommand)command).Length + ", Actual=" + ((PayloadCommand)command).Payload.Length + ")" : "<not carrier>";
            Console.WriteLine("Received command to handle: " + command.CommandId + " (" + command.GetType().Name + "). address = " + address + ", payload = " + payloadInfo);

            IEnumerable<GamePad> pads = new List<GamePad>();
            if (command is AddressedCommand)
                pads = _gamePads.Where(p => p.Address == ((AddressedCommand)command).TargetAddress);

            // Special case: StartGameCommand is broadcasted to all clients
            // TODO: Make a special marker interface for broadcasted commands?
            if (command is StartGameCommand)
                pads = _gamePads.ToList();

            foreach (var gamePad in pads)
                gamePad.HandleCommand(command);

            if (command is IResponsiveCommand)
                SendCommand(((IResponsiveCommand)command).Response(pads.FirstOrDefault()));
        }

        private void Master_VisibleChanged(object sender, EventArgs e)
        {
            _gamePads.ForEach(g => g.Focus());
            this.Focus();
        }

        private void btnSpConfigure_Click(object sender, EventArgs e)
        {
            if (spTeensy.IsOpen)
                spTeensy.Close();
            spTeensy.PortName = cbPort.SelectedItem.ToString();
            spTeensy.Open();
            gbNewPad.Enabled = true;
            gpCommunication.Text = "Communication (Connected, " + spTeensy.PortName + ")";
            lbSpConnectionState.Text = "Connected";
            lbSpConnectionState.ForeColor = Color.DarkGreen;

            tbComLogIn.Clear();
            _currentCommand = null; // Dispose of any data 
        }

        private void btnNewPad_Click(object sender, EventArgs e)
        {
            int address = (int)nudAddress.Value;
            if (_gamePads.Any(g => g.Address == address))
            {
                var result = MessageBox.Show("Address " + address + " is already in use by another game pad. Continue anyways?", "Address in use", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                if (result != DialogResult.Yes)
                    return; // Don't create game pad
            }

            var pad = new GamePad(address);
            pad.Show(this);
            _gamePads.Add(pad);

            nudAddress.Value++;
        }

        private void SendCommand(Command command)
        {
            if (command == null) return;
            var bytes = new List<byte>();

            bytes.Add(command.CommandId);

            if (command is AddressedCommand)
                bytes.Add(((AddressedCommand)command).TargetAddress.Value);

            if (command is PayloadCommand)
            {
                PayloadCommand payloadCommand = (PayloadCommand)command;
                byte[] intBytes = BitConverter.GetBytes(payloadCommand.Length.Value);
                if (BitConverter.IsLittleEndian)
                    Array.Reverse(intBytes);
                bytes.AddRange(intBytes);

                bytes.AddRange(payloadCommand.Payload);
            }

            foreach (byte b in bytes)
                Invoke(new delVoidIntBool(AppendByteToSerialLog), b, false); // false = outbound

            byte[] data = bytes.ToArray();
            spTeensy.Write(data, 0, data.Length);
        }
    }
}
