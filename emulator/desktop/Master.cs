using SuperSimonEmulator.Commands;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO.Ports;
using System.Linq;
using System.Threading;
using System.Windows.Forms;

namespace SuperSimonEmulator
{
    public partial class Master : Form
    {
        private delegate void delVoidIntBool(int i, bool b);
        private delegate void delVoidBool(bool b);
        private delegate void delVoidCommand(Command cmd);

        private byte[] _magicSequence = { 0xDE, 0xAD, 0xBE, 0xEF };
        private byte[] _respMagicSequence = { 0xCA, 0xFE, 0xBA, 0xBE };
        private byte[] _currentSequence = null;
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
                    if (_currentSequence == null)
                    {
                        if (b == _magicSequence[0])
                            _currentSequence = _magicSequence;
                        else
                            _currentSequence = _respMagicSequence;
                    }
                    if (_magicSequenceIndex < _currentSequence.Length)
                    {
                        if (b != _currentSequence[_magicSequenceIndex])
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
                    Invoke(new delVoidBool(NewLine), true); // true = inbound
                    if (_currentSequence != _respMagicSequence)
                        Invoke(new delVoidCommand(HandleCommand), _currentCommand);
                    _currentCommand = null;
                    _currentSequence = null;
                    _magicSequenceIndex = 0;
                }
            }
        }

        private void AppendByteToSerialLog(int b, bool inbound)
        {
            (inbound ? tbComLogIn : tbComLogOut).AppendText("[" + b.ToString("X") + "]");
        }

        private void NewLine(bool inbound)
        {
            (inbound ? tbComLogIn : tbComLogOut).AppendText("\r\n");
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
            gbTestFunctions.Enabled = true;
            gpCommunication.Text = "Communication (Connected, " + spTeensy.PortName + ")";
            lbSpConnectionState.Text = "Connected";
            lbSpConnectionState.ForeColor = Color.DarkGreen;

            tbComLogIn.Clear();
            tbComLogOut.Clear();
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

        private void SendCommand(Command command, bool asHost = false)
        {
            if (command == null) return;
            var bytes = new List<byte>();

            // Start with the magic sequence
            if (!asHost)
                bytes.AddRange(_respMagicSequence);
            else
                bytes.AddRange(_magicSequence);

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
            Invoke(new delVoidBool(NewLine), false); // false = outbound

            byte[] data = bytes.ToArray();
            spTeensy.Write(data, 0, data.Length);
        }

        private void btnClearInbound_Click(object sender, EventArgs e)
        {
            tbComLogIn.Clear();
        }

        private void btnClearOutbound_Click(object sender, EventArgs e)
        {
            tbComLogOut.Clear();
        }

        private void btnCopyInbound_Click(object sender, EventArgs e)
        {
            tbComLogIn.SelectAll();
            tbComLogIn.Copy();
            tbComLogIn.Select(tbComLogIn.Text.Length, 0);
            MessageBox.Show("Copied to clipboard!");
        }

        private void btnCopyOutbound_Click(object sender, EventArgs e)
        {
            tbComLogOut.SelectAll();
            tbComLogOut.Copy();
            tbComLogOut.Select(tbComLogOut.Text.Length, 0);
            MessageBox.Show("Copied to clipboard!");
        }

        private void btnTestDiscover_Click(object sender, EventArgs e)
        {
            SendCommand(new DiscoverCommand(0x00), asHost: true);
            Thread.Sleep(100);
            SendCommand(new DiscoverCommand(0x01), asHost: true);
            Thread.Sleep(100);
            SendCommand(new DiscoverCommand(0x02), asHost: true);
            Thread.Sleep(100);
            SendCommand(new DiscoverCommand(0x03), asHost: true);
            Thread.Sleep(100);
        }

        private void btnTestEcho_Click(object sender, EventArgs e)
        {
            SendCommand(new EchoCommand(0x03), asHost: true);
        }
    }
}
