using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net.Sockets;
using System.Net;
using System.IO;
using System.Threading;

namespace Admin
{
    public partial class Form2 : Form
    {
        TcpClient client; // socket client
        StreamWriter sw;  // streamWriter
        StreamReader sr;  // streamReader
        char[] charArray = new char[1000]; // read char array
        //int Time_till_hint = Form1.Time_till_hint;
        //public static string Hints= Form1.Hints ;
        int port = Form1.port;


        public Form2(TcpClient client_form1)
        {
            InitializeComponent();

            //client = new TcpClient();
            //client.Connect(new IPEndPoint(IPAddress.Parse("192.168.1.29"), port));
            this.client = client_form1;
            sw = new StreamWriter(client.GetStream()); sw.AutoFlush = true;
            sr = new StreamReader(client.GetStream());
            backgroundWorker1.RunWorkerAsync(sr);
            label3.Text = Form1.Time_till_hint.ToString();
            label4.Text = Form1.Hints;

        }

        private void button2_Click(object sender, EventArgs e)
        {
            string msg = textBox1.Text;
            //example: 'Time_to_hint:10'
            if (msg.Contains("Time_till_hint:") && msg.Length>15)
            {
                int new_time;
                string time = msg.Substring(15, msg.Length - 15);
                bool isNumeric = int.TryParse(time, out new_time);
                //int new_time = int.TryParse (msg.Substring(15, msg.Length-15) ) ;
                string new_time_string = new_time.ToString();
                Console.WriteLine(new_time_string + "- the new time");

                if (new_time > 0 && new_time < 80)
                {
                    label3.Text = new_time_string;
                    Form1.Time_till_hint = new_time;
                    //+ "Time_till_hint:"+ new_time
                    sw.WriteLine("Admin_all_" + msg);
                }
                    
                else
                    listBox1.Items.Add("Error- You need to enter a number between 0-80");

            }
                  
            else if (msg.Contains("Hints:"))
            {
                string hinted = msg.Substring(6, msg.Length-6);
                Console.WriteLine(hinted + "- hinted");

                if (hinted == "False" || hinted== "True" )
                {
                    label4.Text = hinted;
                    Form1.Hints = hinted;
                    sw.WriteLine("Admin_all_" + msg);
                    
                }
                   
                else
                    listBox1.Items.Add("Error- You need to enter False/True");

            }
            


        }

        private void backgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {
            StreamReader sr = e.Argument as StreamReader; // get streamReader argument from runWorkerAsync
            var data = "";
            var readByteCount = 0;

            do
            {

                readByteCount = sr.Read(charArray, 0, charArray.Length);

                if (readByteCount > 0)
                {
                    
                    data = new string(charArray, 0, readByteCount);
                    //example: Invoke(new Action(() => listBox1.Items.Add("server: " + data)));
                    Console.WriteLine("data--->" + data);
                    if (data == "bad input")
                        Invoke(new Action(() => listBox1.Items.Add("server: " + data)));



                }
                else Thread.Sleep(100);
                Console.WriteLine(data);
            }
            while (data != "bye");
            Invoke(new Action(() => listBox1.Items.Add("connection terminated") ));
        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.Hide();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            textBox1.Text = button3.Text;
            listBox1.Items.Clear();
            listBox1.Items.Add("Insert time till hint (0-80)");
        }

        private void button4_Click(object sender, EventArgs e)
        {
            textBox1.Text = button4.Text;
            listBox1.Items.Clear();
            listBox1.Items.Add("Insert True/False");
        }

        private void button5_Click(object sender, EventArgs e)
        {
            string msg;

            if (button5.Text == "Stop server auto shut down")
            {
                msg = "stop_auto_shut";
                button5.Text = "Allow server auto shut down";


            }
            else
            {
                msg = "allow_auto_shut";
                button5.Text = "Stop server auto shut down";
            }

            sw.WriteLine("Admin_" + msg);



        }

        private void button6_Click(object sender, EventArgs e)
        {
            string msg = "End_test";
            sw.WriteLine("Admin_" + msg);
        }
    }
    
}
