using EyeTrackerDataScrapper.Properties;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Resources;
using System.Windows.Forms;
using Tobii.Interaction;
using Tobii.Research;
using Tobii.Research.Addons;

namespace EyeTrackerDataScrapper
{
    public partial class Form1 : Form
    {
        //private TcpClient port = new TcpClient("localhost", 4242);
        
        CheckBox lastChecked;
        private int currentQuestion = -1;
        private static readonly int numberOfQuestions = 30;

        private List<String> studentAnswers = initializeStudentAnswers();
        private readonly List<String> correctAnswers = initializeCorrectAnswers();
        private readonly List<String> questions = initializeQuestions();
        private readonly List<List<String>> possibleAnswers = initializePossibleAnswers();

        public Form1()
        {
            InitializeComponent();

            //zapocinje cuvanje ispisa u fajl
            string fileName = DateTime.UtcNow.ToString("log_yyyy-MM-dd", CultureInfo.InvariantCulture) + ".txt";
            FileStream filestream = new FileStream(fileName, FileMode.Create);
            var streamwriter = new StreamWriter(filestream);
            streamwriter.AutoFlush = true;
            Console.SetOut(streamwriter);
            Console.SetError(streamwriter);
            Console.WriteLine("Starting log");

            //pocetna strana
            btnNext.Text = "ZAPOČNI";
            checkBoxA.Visible = false;
            checkBoxB.Visible = false;
            checkBoxC.Visible = false;
            checkBoxD.Visible = false;

            //ConnectToEyeTracker();
        }

        private static List<string> initializeQuestions()
        {
            var f = Resources.pitanja.Split('\n');
            return new List<string>(f);
        }

        private static List<List<string>> initializePossibleAnswers()
        {
            var possibleAnswersList = new List<List<string>>();
            var questions = Resources.mogucnosti.Split('\r');
            foreach (var question in questions)
            {
                possibleAnswersList.Add(new List<string>(question.Replace("\n","").Replace("\r","").Split('|')));
            }
            return possibleAnswersList;
        }

        private static List<string> initializeCorrectAnswers()
        {
            var f = Resources.odgovori.Split(new char[] { '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
            return new List<string>(f);
        }

        private static List<String> initializeStudentAnswers()
        {
            var answerList = new List<String>();
            for(int i = 0; i < numberOfQuestions; i++)
            {
                answerList.Add(" ");
            }

            return answerList;
        }

        private void RefreshPanel()
        {
            txtQuestion.Text = questions[currentQuestion];
            panelCode.BackgroundImage = getCodeImage();
            
            checkBoxA.Text = "(A) " + possibleAnswers[currentQuestion][0];
            checkBoxB.Text = "(B) " + possibleAnswers[currentQuestion][1];
            checkBoxC.Text = "(C) " + possibleAnswers[currentQuestion][2];
            checkBoxD.Text = "(D) " + possibleAnswers[currentQuestion][3];
        }

        private Image getCodeImage()
        {
            switch (currentQuestion)
            {
                case 0:
                    return Resources._1;
                case 1:
                    return Resources._2;
                case 2:
                    return Resources._3;
                case 3:
                    return Resources._4;
                case 4:
                    return Resources._5;
                case 5:
                    return Resources._6;
                case 6:
                    return Resources._7;
                case 7:
                    return Resources._8;
                case 8:
                    return Resources._9;
                case 9:
                    return Resources._10;
                case 10:
                    return Resources._11;
                case 11:
                    return Resources._12;
                case 12:
                    return Resources._13;
                case 13:
                    return Resources._14;
                case 14:
                    return Resources._15;
                case 15:
                    return Resources._16;
                case 16:
                    return Resources._17;
                case 17:
                    return Resources._18;
                case 18:
                    return Resources._19;
                case 19:
                    return Resources._20;
                case 20:
                    return Resources._21;
                case 21:
                    return Resources._22;
                case 22:
                    return Resources._23;
                case 23:
                    return Resources._24;
                case 24:
                    return Resources._25;
                case 25:
                    return Resources._26;
                case 26:
                    return Resources._27;
                case 27:
                    return Resources._28;
                case 28:
                    return Resources._29;
                case 29:
                    return Resources._30;
                default:
                    return new Bitmap("icon.ico");
            }
        }

        private void ConnectToEyeTracker()
        {
            var eyeTracker = EyeTrackingOperations.FindAllEyeTrackers().FirstOrDefault();
            Console.WriteLine("Found eye tracker {0}", eyeTracker.Address);

            var calibrationValidation = new ScreenBasedCalibrationValidation(eyeTracker);

            var points = new NormalizedPoint2D[] {
                new NormalizedPoint2D(0.1f, 0.1f),
                new NormalizedPoint2D(0.1f, 0.9f),
                new NormalizedPoint2D(0.5f, 0.5f),
                new NormalizedPoint2D(0.9f, 0.1f),
                new NormalizedPoint2D(0.9f, 0.9f)
            };

            calibrationValidation.EnterValidationMode();

            foreach (var point in points)
            {
                Console.WriteLine("Collecting for point {0}, {1}", point.X, point.Y);

                calibrationValidation.StartCollectingData(point);
                while (calibrationValidation.State == ScreenBasedCalibrationValidation.ValidationState.CollectingData)
                {
                    System.Threading.Thread.Sleep(25);
                }
            }

            var result = calibrationValidation.Compute();
            Console.WriteLine(calibrationValidation);
            calibrationValidation.LeaveValidationMode();


            // mogucnost 2
            /*
            var host = new Host();
            var gazePointDataStream = host.Streams.CreateGazePointDataStream();
            gazePointDataStream.GazePoint((gazePointX, gazePointY, _) => Console.WriteLine("X: {0} Y:{1}", gazePointX, gazePointY));
            */
        }

        private void CalculateScore()
        {
            int correct = 0;
            for (var i = 0; i < correctAnswers.Count; i++)
            {
                if (studentAnswers[i].Equals(correctAnswers[i]))
                {
                    Console.WriteLine("Pitanje {0} je tačno odgovoreno", i + 1);
                    correct++;
                }
                else
                {
                    Console.WriteLine("Pitanje {0} nije tačno odgovoreno - tačan odgovor je {1}, Vaš odgovor je {2}", i + 1, correctAnswers[i], studentAnswers[i]);
                }
            }

            Console.WriteLine("Tacno odgovorenih {0} \n", correct);
        }


        private void checkBoxA_CheckedChanged(object sender, EventArgs e)
        {
            CheckBox activeCheckBox = sender as CheckBox;
            if (activeCheckBox != lastChecked && lastChecked != null) lastChecked.Checked = false;
            lastChecked = activeCheckBox.Checked ? activeCheckBox : null;            
        }

        private void checkBoxB_CheckedChanged(object sender, EventArgs e)
        {
            CheckBox activeCheckBox = sender as CheckBox;
            if (activeCheckBox != lastChecked && lastChecked != null) lastChecked.Checked = false;
            lastChecked = activeCheckBox.Checked ? activeCheckBox : null;
        }

        private void checkBoxC_CheckedChanged(object sender, EventArgs e)
        {
            CheckBox activeCheckBox = sender as CheckBox;
            if (activeCheckBox != lastChecked && lastChecked != null) lastChecked.Checked = false;
            lastChecked = activeCheckBox.Checked ? activeCheckBox : null;            
        }

        private void checkBoxD_CheckedChanged(object sender, EventArgs e)
        {
            CheckBox activeCheckBox = sender as CheckBox;
            if (activeCheckBox != lastChecked && lastChecked != null) lastChecked.Checked = false;
            lastChecked = activeCheckBox.Checked ? activeCheckBox : null;
        }

        private void btnBack_Click(object sender, EventArgs e)
        {
            //save current checked box
            studentAnswers[currentQuestion] = (lastChecked == null) ? " " : lastChecked.Name.Last().ToString();

            currentQuestion = (currentQuestion <= 0) ? 0 : currentQuestion - 1;

            //redisplay data
            btnNext.Text = "SLEDEĆE";
            RefreshPanel();
            checkBoxA.Checked = studentAnswers[currentQuestion].Equals('A');
            checkBoxB.Checked = studentAnswers[currentQuestion].Equals('B');
            checkBoxC.Checked = studentAnswers[currentQuestion].Equals('C');
            checkBoxD.Checked = studentAnswers[currentQuestion].Equals('D');
            lastChecked = (checkBoxA.Checked) ? checkBoxA : ((checkBoxB.Checked) ? checkBoxB : ((checkBoxC.Checked) ? checkBoxC : ((checkBoxD.Checked) ? checkBoxD : null)));

            //if first question disable back btn
            if (currentQuestion == 0)
            {
                btnBack.Visible = false;
            }

            Console.WriteLine("Current question> {0} at {1}", currentQuestion, DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss.fff", CultureInfo.InvariantCulture));
        }

        private void btnNext_Click(object sender, EventArgs e)
        {
            // save current checked box
            if (currentQuestion > -1)
            {
                studentAnswers[currentQuestion] = (lastChecked == null) ? " " : lastChecked.Name.Last().ToString();
                btnBack.Visible = true;
            } 
            else
            {
                btnNext.Text = "SLEDEĆE";
                checkBoxA.Visible = true;
                checkBoxB.Visible = true;
                checkBoxC.Visible = true;
                checkBoxD.Visible = true;
            }
            

            // is finish question
            if (currentQuestion == numberOfQuestions-1)
            {
                CalculateScore();
                Application.Exit();
                this.Close();
                return;
            }

            currentQuestion++;


            //redisplay data
            
            RefreshPanel();
            checkBoxA.Checked = studentAnswers[currentQuestion].Equals('A');
            checkBoxB.Checked = studentAnswers[currentQuestion].Equals('B');
            checkBoxC.Checked = studentAnswers[currentQuestion].Equals('C');
            checkBoxD.Checked = studentAnswers[currentQuestion].Equals('D');
            lastChecked = (checkBoxA.Checked) ? checkBoxA : ((checkBoxB.Checked) ? checkBoxB : ((checkBoxC.Checked) ? checkBoxC : ((checkBoxD.Checked) ? checkBoxD : null)));

            //if last question rename next btn to finish
            if (currentQuestion == numberOfQuestions-1)
            {
                btnNext.Text = "ZAVRŠI TEST";
            }

            Console.WriteLine("Current question> {0} at {1}", currentQuestion, DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss.fff", CultureInfo.InvariantCulture));
        }
    }
}
