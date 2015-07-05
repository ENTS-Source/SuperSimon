﻿using SuperSimonEmulator.Commands;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SuperSimonEmulator
{
    public partial class Master : Form
    {
        private delegate void delVoidInt(int i);
        private delegate void delVoidCommand(Command cmd);

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
                Invoke(new delVoidInt(AppendByteToSerialLog), b);

                if (_currentCommand == null)
                {
                    _currentCommand = CommandRegistry.FindCommand(b);
                    if (_currentCommand == null)
                    {
                        Console.WriteLine("Failed to find command for ID: " + b+", ignoring byte.");
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
                }
            }
        }

        private void AppendByteToSerialLog(int b)
        {
            tbLog.AppendText(b.ToString());
        }

        private void HandleCommand(Command command)
        {
            // TODO: Actually handle command
            string address = command is AddressedCommand ? ((AddressedCommand)command).TargetAddress.ToString() : "<not addressed>";
            string payloadInfo = command is PayloadCommand ? "(Length=" + ((PayloadCommand)command).Length + ", Actual=" + ((PayloadCommand)command).Payload.Length + ")" : "<not carrier>";
            Console.WriteLine("Received command to handle: " + command.CommandId + ". address = " + address + ", payload = " + payloadInfo);
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

            tbLog.Clear();
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
    }
}