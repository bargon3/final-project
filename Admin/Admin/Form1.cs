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
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text.RegularExpressions;

namespace Admin
{
    public partial class Form1 : Form
    {
        TcpClient client; // socket client
        StreamWriter sw;  // streamWriter
        StreamReader sr;  // streamReader
        char[] charArray = new char[100000]; // read char array
        int ticks;
        private string secret_code = "8642";
        public static int port = 58456;


        /// <summary>
        /// belongs to the share screen
        /// </summary>
        public static Bitmap bmpScreenshot;
        public bool start = false;
        public bool can_share = true;
        public static Graphics gfxScreenshot;
        int countRead = 0, countWrite = 0;
        TcpClient client2 = null;
        TcpListener socket = null;
        int p;

        List<User> Users1 = new List<User>();
        int last_ID = 0;
        public static int Time_till_hint = 20;
        public static string Hints= "True";
        Image off_screen_image = Image.FromFile("E:/YB project/closed screen.jpg");







        public Form1()
        {
            InitializeComponent();

            client = new TcpClient();
            client.Connect(new IPEndPoint(IPAddress.Parse("192.168.1.29"), port));
            sw = new StreamWriter(client.GetStream()); sw.AutoFlush = true;
            sr = new StreamReader(client.GetStream());
            label1.Text = "connection established";
            timer1.Start();
            backgroundWorker1.RunWorkerAsync(sr);
            sw.Write("I am Admin" +secret_code);
            label22.Text = Time_till_hint.ToString();
            pictureBox1.BackColor = Color.Gray;
            pictureBox1.Image = off_screen_image;


        }

        private void button1_clicked(object sender, EventArgs e)
        {

            // sending example  sw.WriteLine(My_level.Text + "-" + listBox1.Items[1] + "-" + textBox1.Text);
            Console.WriteLine("Enterted get status");
            sw.WriteLine("Admin_update");

            //var users = this.Users;
            //dataGridView1.DataSource = users;

        }

        private void backgroundWorker1_DoWork(object sender, DoWorkEventArgs e) // receive msg
        {
            StreamReader sr = e.Argument as StreamReader; // get streamReader argument from runWorkerAsync
            var data = "";
            var readByteCount = 0;
            string[] details; string[] users_superated;
            Console.WriteLine("qweweqwqe");


            do
            {


                readByteCount = sr.Read(charArray, 0, charArray.Length);

                if (readByteCount > 0)
                {
                    data = new string(charArray, 0, readByteCount);
                    Console.WriteLine(data);

                    if (data.Contains("Share_screen_user_gone"))
                    {
                        //recievingWorker.RunWorkerCompleted += new RunWorkerCompletedEventHandler(recievingWorker_RunWorkerCompleted);  //--- לא עובד
                        //recievingWorker.CancelAsync();
                        Console.WriteLine("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++");
                        //this.client2.Close();
                        //this.socket.Stop();
                        this.can_share = false;
                        //dataGridView1_RowHeaderMouseClick(); /////
                        pictureBox1.BackColor = Color.Salmon;
                        string message = "The share screen stoped, the user disconnected";
                        string title = "Alert";
                        MessageBox.Show(message, title);
                        string msg = "Admin_Good";
                        sw.WriteLine(msg);
                    }

                    else if (data.Contains("man"))
                    {
                        string message = "Got it";
                        string title = "Alert";
                        MessageBox.Show(message, title);

                    }
                    //example: "User_chat-Noam-I am ok" //example: "User_chat_all-Noam-I am ok"
                    else if ( data.Contains("User_chat"))
                    {

                        string name = data.Split('-')[1];
                        string msg = data.Split('-')[2];
                        int Lines_num = listBox3.Items.Count;

                        if ( data.Contains("_all") )
                        {
                            if ( Lines_num > 0 && listBox3.Items[0].ToString().Contains("Broadcast") )
                            {
                                Invoke(new Action(() => listBox3.Items.Add(name + ": " + msg)));
                            }

                            else
                            {
                                switch (MessageBox.Show(name + " wrote a Broadcast message, would you like to see and join the chat?",
                                                  "Notification",
                                                  MessageBoxButtons.YesNo,
                                                  MessageBoxIcon.Question))
                                {
                                    case DialogResult.Yes:
                                        // (Yes)

                                        Invoke(new Action(() => listBox3.Items.Clear()));
                                        Invoke(new Action(() => listBox3.Items.Add("Broadcast >")));
                                        Invoke(new Action(() => listBox3.Items.Add("")));
                                        Invoke(new Action(() => listBox3.Items.Add(name + ":" + msg)));
                                        break;

                                    case DialogResult.No:
                                        // (No)                                   
                                        break;
                                }
                            }
                         

                        }
                      

                        else if (Lines_num > 0 && listBox3.Items[0].ToString().Contains(name) )
                        {
                            Invoke(new Action(() => listBox3.Items.Add(name + ": " + msg)));
                        }

                        else
                        {
                            switch (MessageBox.Show( name + " wrote you a message would you like to chat with him?",
                                                    "Notification",
                                                    MessageBoxButtons.YesNo,
                                                    MessageBoxIcon.Question))
                            {
                                case DialogResult.Yes:
                                    // (Yes)

                                    Invoke(new Action(() => listBox3.Items.Clear() ));
                                    Invoke(new Action(() => listBox3.Items.Add("Chat with user >" + name )));
                                    Invoke(new Action(() => listBox3.Items.Add("")));
                                    Invoke(new Action(() => listBox3.Items.Add(name + ":" + msg) ));
                                    break;

                                case DialogResult.No:
                                    // (No)                                   
                                    break;
                            }
                        }

                    }

                    else
                    {

                        Console.WriteLine("deqdidwqi");
                        //example: Invoke(new Action(() => listBox1.Items.Add("server: " + data)));

                        // splits to every user
                        users_superated = data.Split('/');
                        int amount = users_superated.Length - 1;
                        // checking if there is knew  users

                        int x = 0;
                        //Invoke(new Action(() => listBox1.Items.Clear() ));
                        foreach (User user in Users1)
                        {
                            details = users_superated[x].Split('-');
                            user.Update(details);
                            x++;
                        }



                        if (amount > last_ID)
                        {

                            for (int i = last_ID; i < amount; i++)
                            {
                                // split every user to his details
                                details = users_superated[i].Split('-');
                                Invoke(new Action(() => label1.Text = details.Length.ToString()));
                                Invoke(new Action(() => this.Users1.Add(new User()
                                {
                                    ID = details[1],
                                    Name = details[3],
                                    Subj = details[5],
                                    Units = details[7],
                                    Cur_level = details[9],
                                    Cur_ques = details[11],
                                    L_grade = details[13],
                                    T_grade = details[15],
                                    History = details[17],
                                    Last_entry = details[19]

                                })

                                    ));
                            }

                            last_ID = amount;

                        }



                        var users = Users1;
                        BindingSource source = new BindingSource();
                        source.DataSource = users;

                        Invoke(new Action(() => dataGridView1.DataSource = source));
                        Invoke(new Action(() => dataGridView1.Columns["Units"].Visible = false));
                        Invoke(new Action(() => dataGridView1.Columns["L_grade"].Visible = false));
                        Invoke(new Action(() => dataGridView1.Columns["T_grade"].Visible = false));
                        Invoke(new Action(() => dataGridView1.Columns["History"].Visible = false));
                        Invoke(new Action(() => dataGridView1.Columns["Last_entry"].Visible = false));


                    }


                }
                else Thread.Sleep(100);
                Console.WriteLine(data);
                


            }
            while (data != "bye");
            Invoke(new Action(() => label1.Text = "connection terminated"));
        }

        private void backgroundWorker1_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            client.Close();
        }


//-------------------------------------------------------------------------------------------------------------------- share screens

        // show screen button- starting sharing screens, example: Share_screen-Noam
        private void button8_Click(object sender, EventArgs e)
        {
            can_share = false;
            Thread.Sleep(5000);
            p = FreeTcpPort();
            Console.WriteLine("portttt   " + p.ToString());

            string Choosen_Name = label5.Text;
            string msg;
            if (Choosen_Name != "")
            {
                //finds the user with this name
                User result = Users1.Find(x => x.GetName() == Choosen_Name);
                //button8.Enabled = false;
                this.start = true;
                can_share = true;
                msg = "Share_screen-" + Choosen_Name + "-" + p.ToString();
                sw.WriteLine("Admin_" + msg);



            }

            else
            {
                string message = "please choose a user";
                string title = "Error";
                MessageBox.Show(message, title);
            }

            recievingWorker.RunWorkerAsync();
        }

        public void imageFromByteArray(byte[] arr)

        { // bytearray to image and display in picturebox
            countRead++;
            //Console.WriteLine("converting byte array to picturebox {0}", countRead);
            MemoryStream mStream = new MemoryStream();
            mStream.Write(arr, 0, Convert.ToInt32(arr.Length));
            pictureBox1.Image = new Bitmap(mStream, false);
            mStream.Dispose();
        }


        private void recievingWorker_DoWork(object sender, DoWorkEventArgs e)
        {
            // connection--->
            Console.WriteLine("start server");
            TcpListener serverSocket = new TcpListener(IPAddress.Parse("192.168.1.29"), p);
            serverSocket.Start();
            Console.WriteLine("started socket");
            TcpClient client3 = serverSocket.AcceptTcpClient();
            Console.WriteLine("receive tcp by server");
            this.client2 = client3;
            this.socket = serverSocket;
           

            while (can_share == true)
            {
                try
                {
                    NetworkStream netStream = client2.GetStream();
                    if (netStream.DataAvailable)
                    {

                        BinaryFormatter bf = new BinaryFormatter();
                        byte[] bytes = (byte[])bf.Deserialize(netStream);
                        imageFromByteArray(bytes);
                    }
                }

                catch
                {
                    Console.WriteLine("SHARE SCREEN PROBLEM");
                    break;
                }
                          

                
            }
            

        }

        private void recievingWorker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            Console.WriteLine(">>>>>>>>>");
            listBox3.Items.Add("finished recieving worker");
            this.client2.Close();
            this.socket.Stop();
            pictureBox1.Image = off_screen_image;

        }

        //--------------------------------------------------------------------------------------------------------------------


        private void button2_Click(object sender, EventArgs e)
        {
            Form2 newform = new Form2(client);
            newform.ShowDialog();
            //Hints= Form2


            bool cur_hint;

            if (Hints == "True")
                cur_hint = true;
            else
                cur_hint = false;

            label22.Text = Time_till_hint.ToString();

            foreach (User user in Users1)          
                    user.Time_till_hint = Time_till_hint;
            

            foreach (User user in Users1)
                    user.Hints = cur_hint;
            

            //listBox3.Items.Add(Hints);
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            ticks++;
            if (ticks == 100)
            {
                Console.WriteLine("TIme to update");
                ticks = 0;
                button1_clicked(sender, e);
            }

        }

        // shut down button (to 1 user)
        private void button5_Click(object sender, EventArgs e)
        {
            string Choosen_Name = label5.Text;
            if (Choosen_Name != "")
            {
                string msg = "Shutdown-" + Choosen_Name;
                sw.WriteLine("Admin_" + msg);
            }

            else
            {
                string message = "please choose a user";
                string title = "Error";
                MessageBox.Show(message, title);
            }

        }

        // stop hints button (to 1 user)
        private void button6_Click(object sender, EventArgs e)
        {
            string Choosen_Name = label5.Text;
            string msg;
            if (Choosen_Name != "")
            {
                //finds the user with this name
                User result = Users1.Find(x => x.GetName() == Choosen_Name);

                if (button6.Text == "Block hints")
                {
                    msg = "private_Hints-False-" + Choosen_Name;
                    button6.Text = "Allow hints";
                    result.Hints = false;
                }


                else
                {
                    msg = "private_Hints-True-" + Choosen_Name;
                    button6.Text = "Block hints";
                    result.Hints = true;
                }
                   
                sw.WriteLine("Admin_" + msg);


            }

            else
            {
                string message = "please choose a user";
                string title = "Error";
                MessageBox.Show(message, title);
            }
        }

        private void button7_Click(object sender, EventArgs e)
        {
            string Choosen_Name = label5.Text;
            string msg;
            if (Choosen_Name != "")
            {
                //example: 'private_Time_till_hint-25-Noam'
                //finds the user with this name
                User result = Users1.Find(x => x.GetName() == Choosen_Name);

               
                button6.Text = "Allow hints";
                

                int new_time;
                string time = textBox1.Text;
                bool isNumeric = int.TryParse(time, out new_time);
                string new_time_string = new_time.ToString();
                Console.WriteLine(new_time_string + "- the new time");

                if (new_time > 0 && new_time < 80)
                {
                    label3.Text = new_time_string;
                    msg = "private_Time_till_hint-" + new_time_string + "-" +Choosen_Name;
                    result.Time_till_hint = new_time;
                    textBox1.Text = "";
                    label22.Text = new_time_string;
                    sw.WriteLine("Admin_" + msg);
                }

                else
                {
                    string message = "Error- You need to enter a number between 0-80";
                    string title = "Error";
                    MessageBox.Show(message, title);
                }

            }

            else
            {
                string message = "please choose a user";
                string title = "Error";
                MessageBox.Show(message, title);
            }

        }

        private void button3_Click(object sender, EventArgs e)
        {

            int Lines_num = listBox3.Items.Count;
            string msg;

            if (Lines_num > 0 )
            {
                if (listBox3.Items[0].ToString().Contains("Broadcast"))
                {
                    msg = "to_all_Broadcast" + "-" + textBox2.Text;

                }
                else
                {
                    string Choosen_Name = listBox3.Items[0].ToString().Split('>')[1];
                    msg = "private_chat-" + Choosen_Name + "-" + textBox2.Text;
                }

                listBox3.Items.Add("You: " + textBox2.Text);
                textBox2.Text = "";
                sw.WriteLine("Admin_" +  msg);
            }          
         

            else
            {
                string message = "please choose a user";
                string title = "Error";
                MessageBox.Show(message, title);
            }
 

        }

        private void button4_Click(object sender, EventArgs e)
        {
            listBox3.Items.Clear();
            listBox3.Items.Add("-------Broadcast >");
        }

        private void dataGridView1_RowHeaderMouseClick(object sender, DataGridViewCellMouseEventArgs e)
        {
            try
            {
                var selectedUser = dataGridView1.SelectedRows[0].DataBoundItem as User;
                string info = selectedUser.ToString();
                label3.Text = selectedUser.ID;
                label5.Text = selectedUser.Name;
                label7.Text = selectedUser.Subj;
                label9.Text = selectedUser.Units;
                label10.Text = selectedUser.Cur_level;
                label12.Text = selectedUser.Cur_ques;
                label14.Text = selectedUser.T_grade;
                label16.Text = selectedUser.L_grade;
                label18.Text = selectedUser.History;
                label20.Text = selectedUser.Last_entry;
                label22.Text = selectedUser.Time_till_hint.ToString();

                if (selectedUser.Hints == true)
                    button6.Text = "Block hints";
                else
                    button6.Text = "Allow hints";

                listBox3.Items.Clear();
                listBox3.Items.Add("-------chat with user >"+ selectedUser.Name);

            }

            catch (Exception ex)
            {
                MessageBox.Show("some error ocured: " + ex.Message + '-' + ex.Source);
            }
        }

        static int FreeTcpPort()
        {
            TcpListener l = new TcpListener(IPAddress.Loopback, 0);
            l.Start();
            int port = ((IPEndPoint)l.LocalEndpoint).Port;
            l.Stop();
            return port;
        }

    }
}
