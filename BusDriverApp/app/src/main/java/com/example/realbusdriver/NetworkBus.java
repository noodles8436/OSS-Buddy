package com.example.realbusdriver;


import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.SocketTimeoutException;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;

public class NetworkBus {


    private static SocketChannel client;
    private static NetworkBus instance;

    private static String address = "115.86.19.194";
    private static int port = 7788;

    private static String driverName;
    private static String driverUID;
    private static String driverVehicleNo;
    private static String driverRouteNo;

    public static NetworkBus start() {
        if (instance == null)
            instance = new NetworkBus();
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


    private NetworkBus() {
        init();
    }

    private static void init() {
        try {
            client = SocketChannel.open(new InetSocketAddress(address, port));
            // client.socket().setSoTimeout(PROTOCOL.READ_TIME_OUT);
        } catch (IOException e) {

            e.printStackTrace();

        }
    }

    // API

    public static boolean register() {
        String sendMsg = PROTOCOL_BUS.BUSDRIVER_REGISTER + PROTOCOL_BUS.TASK_SPLIT + getDriverVehicleNo() +
                PROTOCOL_BUS.TASK_SPLIT + getDriverName() + PROTOCOL_BUS.TASK_SPLIT + getDriverUID();
        send(sendMsg);

        String recvMsg = recv();

        try {
            stop();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        init();

        if(recvMsg.equals(PROTOCOL_BUS.BUSDRIVER_LOGIN_SUCCESS)) {
            return true;
        }else {
            return false;
        }
    }

    public static boolean login() {
        String sendMsg = PROTOCOL_BUS.BUSDRIVER_LOGIN + PROTOCOL_BUS.TASK_SPLIT + getDriverVehicleNo() +
                PROTOCOL_BUS.TASK_SPLIT + getDriverName() + PROTOCOL_BUS.TASK_SPLIT + getDriverUID() +
                PROTOCOL_BUS.TASK_SPLIT + getDriverRouteNo();
        send(sendMsg);

        String recvMsg = recv();

        if (recvMsg.equals(PROTOCOL_BUS.BUSDRIVER_LOGIN_SUCCESS)){
            return true;
        } else if(recvMsg.equals(PROTOCOL_BUS.BUSDRIVER_LOGIN_FAIL)) {
            return false;
        } else if(recvMsg.equals(PROTOCOL_BUS.BUSDRIVER_LOGIN_ERR)) {
            return false;
        }else {
            return false;
        }
    }


    //String = [정거장 이름 , 남은 정거장 수]
    public static BusReserve getReserveStation() {
        String recvMsg = recv();
        String[] recvResult = recvMsg.split(PROTOCOL_BUS.TASK_SPLIT);
        System.out.println("yeayea");
        String[] result = new String[2];
        if(recvResult[0].equals(PROTOCOL_BUS.BUSDRIVER_NODE_ANNOUNCE)) {
            BusReserve bus = new BusReserve(recvResult[1], Integer.parseInt(recvResult[2]));
            return bus;
        }else {
            return null;
        }
    }


    // low-level Server-Client API

    private static void send(String msg) {
        try {

            ByteBuffer buffer = ByteBuffer.allocate(PROTOCOL_BUS.SERVER_PACKET_SIZE);
            buffer = ByteBuffer.wrap(msg.getBytes());
            client.write(buffer);

        } catch (IOException e) {

            e.printStackTrace();

        }
    }

    private static String recv() {
        try {

            String response = null;
            ByteBuffer buffer = ByteBuffer.allocate(PROTOCOL_BUS.SERVER_PACKET_SIZE);
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

    // Please Fill methods below

    public static void setDriverName(String name) {
        driverName = name;
    }

    public static void setDriverVehicleNo(String phone) {
        driverVehicleNo = phone;
    }

    public static void setDriverUID(String UID) {
        driverUID = UID;
    }

    public static void setDriverRouteNo(String RouteNo) {
        driverRouteNo = RouteNo;
    }

    public static String getDriverName() {
        return driverName;
    }

    public static String getDriverVehicleNo() {
        return driverVehicleNo;
    }

    public static String getDriverUID() {
        return driverUID;
    }

    public static String getDriverRouteNo(){
        return driverRouteNo;
    }

}