package oss;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.SocketTimeoutException;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;

public class GPS extends Thread{
	
	private static SocketChannel gps_client;
	private static String address;
	private static int port;
	
	private static GPS instance;
	private static boolean isRun;
	
	public GPS(String address, int port) {
		this.address = address;
		this.port = port;
	}
	
	public static GPS initGPS(String address, int port) {
		if(instance == null) {
			instance = new GPS(address, port);
		}
		return instance;
	}
	
	public void run() {
		isRun = true;
		
		try {
			gps_client = SocketChannel.open(new InetSocketAddress(address, port));
			// client.socket().setSoTimeout(PROTOCOL.READ_TIME_OUT);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		while(isRun) {
			if(loginGPS()) {
				while(isRun) {
					String sendMsg = PROTOCOL.USER_GPS_DATA + PROTOCOL.TASK_SPLIT;
					sendMsg += Double.toString(Network.getUserLati()) + PROTOCOL.TASK_SPLIT;
					sendMsg += Double.toString(Network.getUserLong());
					System.out.println(sendMsg);
					send(sendMsg);
					try {
						Thread.sleep(1000);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
				}
			}
		}
	}
	
	private static boolean loginGPS() {
		String sendMsg = PROTOCOL.USER_GPS_LOGIN + PROTOCOL.TASK_SPLIT + Network.getUserName() 
		+ PROTOCOL.TASK_SPLIT + Network.getUserPhone() + PROTOCOL.TASK_SPLIT + Network.getUserMac();
		send(sendMsg);
		
		String recvMsg = recv();
		System.out.println(recvMsg);
		if(recvMsg.equals(PROTOCOL.USER_GPS_LOGIN_SUCCESS)) {
			return true;
		}else {
			return false;
		}
	}
	
	public static void stopGPS() {
		isRun = false;
	}
	
	private static void send(String msg) {
		try {
			ByteBuffer buffer = ByteBuffer.allocate(PROTOCOL.PACKET_SIZE);
			buffer = ByteBuffer.wrap(msg.getBytes());
			gps_client.write(buffer);
			
		} catch (IOException e) {
			
			e.printStackTrace();
			
		}
	}
	
	private static String recv() {
		try {
			
			String response = null;
			ByteBuffer buffer = ByteBuffer.allocate(PROTOCOL.PACKET_SIZE);
			gps_client.read(buffer);
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
