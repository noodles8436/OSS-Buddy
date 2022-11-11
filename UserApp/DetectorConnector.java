package com.djy.budy;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.SocketTimeoutException;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;
import java.util.ArrayList;

public class DetectorConnector {


    private static SocketChannel client;
    private static DetectorConnector instance;

    private static String address = "devktw8436.iptime.org";
    private static int port = 9999;

    private static ArrayList<byte[]> images = new ArrayList<byte[]>();

    private static Thread imgMgr;

    private static int sitCnt = 0;

    private static DataOutputStream dos;

    public static DetectorConnector start() {
        if (instance == null)
            instance = new DetectorConnector();
        return instance;
    }

    public static void stop() throws IOException{
        client.close();
    }

    public static void restart() throws IOException{
        stop();
        instance = null;
        start();
    }

    private DetectorConnector() {
        init();
    }

    private static void init() {
        try {

            client = SocketChannel.open(new InetSocketAddress(address, port));
            dos = new DataOutputStream(client.socket().getOutputStream());

            imgMgr = new Thread(){
              public void run(){
                  while(true){
                      if(images.size() >= 4){
                          for(int i = 0; i < 4; i++){
                              sendBytes(images.get(i));
                          }
                          images = new ArrayList<byte[]>();
                          String recv = recv();
                          setSitCnt(Integer.parseInt(recv));
                      }

                  }
              }
            };

            imgMgr.start();

        } catch (IOException e) {

            e.printStackTrace();

        }
    }

    public static boolean login() {
        String sendMsg = PROTOCOL.CLIENT_LOGIN;
        send(sendMsg);

        String recvMsg = recv();

        if (recvMsg.equals(PROTOCOL.CLIENT_LOGIN_SUCCESS)){
            return true;
        }else{
            return false;
        }
    }

    public static void inputImages(byte[] img){
        images.add(img);
    }

    public static void setSitCnt(int sitCnt){
        sitCnt = sitCnt;
    }

    public static int getSitCnt(){
        return sitCnt;
    }


    // low-level Server-Client API

    private static void send(String msg) {
        try {

            ByteBuffer buffer = ByteBuffer.allocate(PROTOCOL.PACKET_SIZE);
            buffer = ByteBuffer.wrap(msg.getBytes());
            client.write(buffer);


        } catch (IOException e) {

            e.printStackTrace();

        }
    }

    private static void sendBytes(byte[] data){
        try{
            //ByteBuffer buffer = ByteBuffer.allocate(PROTOCOL.GLOBAL_PACKET_SIZE);
            //buffer = ByteBuffer.wrap(data);
            //client.write(buffer);
            dos.write(data);
            dos.flush();
        } catch (IOException e){

            e.printStackTrace();

        }
    }

    private static String recv() {
        try {
            String response = null;
            ByteBuffer buffer = ByteBuffer.allocate(PROTOCOL.PACKET_SIZE);
            client.read(buffer);
            response = new String(buffer.array()).trim();
            return response;

        } catch (SocketTimeoutException timeout) {
            return null;

        } catch (IOException ioexcept) {

            ioexcept.printStackTrace();
            return null;

        }
    }

}