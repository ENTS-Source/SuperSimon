using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SuperSimonEmulator
{
    public partial class GamePad : Form
    {
        private List<Button> _pads = new List<Button>();
        private List<Label> _sequenceIcons = new List<Label>();
        private Color _defSequenceColor = Color.LightGray;

        private Color[] _colorMap = {
            Color.FromArgb(170, 0, 0),          // Pad 1 (red)
            Color.FromArgb(59, 170, 0),         // Pad 2 (green)
            Color.FromArgb(255, 255, 255),      // Pad 3 (white)
            Color.FromArgb(224, 220, 0),        // Pad 4 (yellow)
            Color.FromArgb(14, 0, 170)          // Pad 5 (blue)
        };

        public int Address { get; private set; }

        public GamePad(int address)
        {
            if (address < 0 || address > 255)
                throw new ArgumentOutOfRangeException("address");
            Address = address;

            InitializeComponent();
            Text = "Simon Game Pad (Address = " + address + ")";
        }

        private void GamePad_Load(object sender, EventArgs e)
        {
            _pads.Add(btnPad1);
            _pads.Add(btnPad2);
            _pads.Add(btnPad3);
            _pads.Add(btnPad4);
            _pads.Add(btnPad5);

            _sequenceIcons.Add(lbSeq1);
            _sequenceIcons.Add(lbSeq2);
            _sequenceIcons.Add(lbSeq3);
            _sequenceIcons.Add(lbSeq4);
            _sequenceIcons.Add(lbSeq5);
            _sequenceIcons.Add(lbSeq6);
            _sequenceIcons.Add(lbSeq7);
            _sequenceIcons.Add(lbSeq8);
            _sequenceIcons.Add(lbSeq9);
            _sequenceIcons.Add(lbSeq10);
            _sequenceIcons.Add(lbSeq11);

            for (int i = 0; i < _pads.Count; i++)
                _pads[i].BackColor = _colorMap[i];

            SetPadsEnabled(false);
            _sequenceIcons.ForEach(i => i.BackColor = _defSequenceColor);
        }

        private void SetPadsEnabled(bool enabled)
        {
            _pads.ForEach(p => p.Enabled = enabled);
        }
    }
}
