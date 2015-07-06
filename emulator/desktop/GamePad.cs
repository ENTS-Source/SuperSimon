using SuperSimonEmulator.Commands;
using SuperSimonEmulator.Commands.Concrete;
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
        private delegate void delVoidVoid();

        private List<Button> _pads = new List<Button>();
        private List<Label> _sequenceIcons = new List<Label>();
        private Color _defSequenceColor = Color.LightGray;

        private int _sequenceIndex;
        private DateTime _lastPress;

        private List<short> _sequenceTimings = new List<short>();
        private List<byte> _sequenceOrder = new List<byte>();

        private Color[] _colorMap = {
            Color.FromArgb(170, 0, 0),          // Pad 1 (red)
            Color.FromArgb(59, 170, 0),         // Pad 2 (green)
            Color.FromArgb(255, 255, 255),      // Pad 3 (white)
            Color.FromArgb(224, 220, 0),        // Pad 4 (yellow)
            Color.FromArgb(14, 0, 170)          // Pad 5 (blue)
        };

        public int Address { get; private set; }
        public bool JoinedGame { get; private set; }
        public bool CurrentGameComplete { get; private set; }

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

        private void ClearDisplayedSequence()
        {
            _sequenceIcons.ForEach(l =>
            {
                l.BackColor = _defSequenceColor;
                l.Text = "";
            });
        }

        private void UpdateGameUi()
        {
            ClearDisplayedSequence();

            int maximum = Math.Min(_sequenceIcons.Count, _sequenceOrder.Count - _sequenceIndex);
            for (int i = 0; i < maximum; i++)
                SetSequenceLabel(i, _sequenceOrder[_sequenceIndex + i]);
        }

        private void SetSequenceLabel(int seqIndex, int button)
        {
            var label = _sequenceIcons[seqIndex];
            label.Text = "B" + (button);
            label.BackColor = _colorMap[button - 1];
        }

        public GameCompletedCommand CreateCompletedCommand()
        {
            var cmd = new GameCompletedCommand(0xFF); // Target address does not matter - it just needs to be set
            for (int i = 0; i < _sequenceOrder.Count; i++)
                cmd.AddTiming(_sequenceOrder[i], _sequenceTimings[i]);
            return cmd;
        }

        public void HandleCommand(Command command)
        {
            if (command is GameBoardInformationCommand)
                ReadGameBoard((GameBoardInformationCommand)command);
            else if (command is StartGameCommand)
            {
                SetPadsEnabled(true);
                _lastPress = DateTime.Now;
            }
        }

        private void ReadGameBoard(GameBoardInformationCommand command)
        {
            CurrentGameComplete = false;
            _sequenceOrder.Clear();
            _sequenceTimings.Clear();
            foreach (byte p in command.Payload)
            {
                _sequenceOrder.Add(p);
                _sequenceTimings.Add(-1);
            }

            _sequenceIndex = 0;
            Invoke(new delVoidVoid(UpdateGameUi));
        }

        private void btnJoin_Click(object sender, EventArgs e)
        {
            JoinedGame = !JoinedGame;
            btnJoin.Text = JoinedGame ? "Leave Game" : "Join Game";
        }

        private void btnPad_Click(object sender, EventArgs e)
        {
            if (!(sender is Button)) return;
            Button button = (Button)sender;

            byte expectedButton = _sequenceOrder[_sequenceIndex];
            byte buttonId = (byte)(int)button.Tag; // Need a double case to go from object -> int -> byte

            if (expectedButton == buttonId)
            {
                _sequenceTimings[_sequenceIndex] = (short)(DateTime.Now - _lastPress).TotalMilliseconds;
                _lastPress = DateTime.Now;
                _sequenceIndex++;
                if (_sequenceIndex >= _sequenceOrder.Count)
                {
                    CurrentGameComplete = true;
                    SetPadsEnabled(false);
                    MessageBox.Show("Round Completed!", "Round Complete", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                UpdateGameUi();
            }
            else
            {
                CurrentGameComplete = true;
                SetPadsEnabled(false);
                MessageBox.Show("YOU FAILED", "Round Complete", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
