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

        private List<GamePad> _gamePads = new List<GamePad>();

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
                int b = spTeensy.ReadByte();
                Invoke(new delVoidInt(AppendByteToSerialLog), b);
            }
        }

        private void AppendByteToSerialLog(int b)
        {
            tbLog.AppendText(b.ToString());
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
