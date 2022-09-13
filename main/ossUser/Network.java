package ossUser;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.SocketTimeoutException;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;
import java.util.ArrayList;

import ossUser.Network;

public class Network {
	
	
	private static SocketChannel client;
	private static Network instance;
	private static GPS gps;
	
	private static String address = "115.86.19.194";
	private static int port = 7788;
	
	private static String userName;
	private static String userPhone;
	private static String userUID;
	
	private static double _lati;
	private static double _long;
	
	public static Network start() {
		if (instance == null)
			instance = new Network();
		if (gps == null)
			gps = GPS.initGPS(address, port);
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
	
	
	private Network() {
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
		String sendMsg = PROTOCOL.USER_REGISTER+ PROTOCOL.TASK_SPLIT + getUserName() 
		+ PROTOCOL.TASK_SPLIT + getUserPhone() + PROTOCOL.TASK_SPLIT + getUserUID();
		send(sendMsg);
		
		String recvMsg = recv();
		
		try {
			stop();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		init();
		
		if(recvMsg.equals(PROTOCOL.USER_REGISTER_SUCCESS)) {
			return true;
		}else {
			return false;
		}
	}
	
	public static boolean login() {
		String sendMsg = PROTOCOL.USER_LOGIN + PROTOCOL.TASK_SPLIT + getUserName() 
			+ PROTOCOL.TASK_SPLIT + getUserPhone() + PROTOCOL.TASK_SPLIT + getUserUID();
		send(sendMsg);
		
		String recvMsg = recv();
		
		if (recvMsg.equals(PROTOCOL.USER_LOGIN_SUCCESS)){
			gps.start();
			return true;
		} else if(recvMsg.equals(PROTOCOL.USER_LOGIN_FAIL)) {
			GPS.stopGPS();
			return false;
		} else if(recvMsg.equals(PROTOCOL.USER_LOGIN_SERVER_ERR)) {
			GPS.stopGPS();
			return false;
		} else if(recvMsg.equals(PROTOCOL.USER_LOGIN_CLIENT_ERR)) {
			GPS.stopGPS();
			return false;
		}else {
			GPS.stopGPS();
			return false;
		}
	}
	
	public static boolean readyforLocation() {
		while(true) {
			String recvMsg = recv();
			if(recvMsg.equals(PROTOCOL.CONNECTION_CHECK)) {
				send(PROTOCOL.CONNECTION_CHECK);
			}else if(recvMsg.equals(PROTOCOL.KICK_USER)) {
				return false;
			}else if(recvMsg.equals(PROTOCOL.USER_LOCATION_FIND_SUCCESS)) {
				return true;
			}
		}
	}

	public static ArrayList<BusArrival> getBusList(){
		String sendMsg = PROTOCOL.USER_REQ_BUS_LIST;
		send(sendMsg);
		String recvMsg = recv();
		String[] msgResult = recvMsg.split(PROTOCOL.TASK_SPLIT);
		ArrayList<BusArrival> result = new ArrayList<BusArrival>();
		
		
		if(msgResult[0].equals(PROTOCOL.USER_REQ_BUS_LIST)) {
			
			int cnt = Integer.parseInt(msgResult[1]);
			
			if(cnt > 0) {
				
				for(int i = 2; i < cnt + 2; i++) {
					String[] busData = msgResult[i].split(":");
					BusArrival busArr = new BusArrival(busData[0], Integer.parseInt(busData[1]));
					result.add(busArr);
				}
				
			}
			
		}
		
		return result;
		
	}
	
	public static boolean isPossibleBus(String routeNo) {
		String sendMsg = PROTOCOL.USER_BUS_CAN_RESERVATION + PROTOCOL.TASK_SPLIT
				+ routeNo;
		send(sendMsg);
		String recvMsg = recv();
		
		if(recvMsg.equals(PROTOCOL.USER_BUS_CAN_RESERVATION_OK)) {
			return true;
		}else {
			return false;
		}
	}
	
	public static boolean reserveBus(String routeNo) {
		String sendMsg = PROTOCOL.USER_BUS_RESERVATION_CONFIRM + PROTOCOL.TASK_SPLIT
				+ routeNo;
		send(sendMsg);
		
		String recvMsg = recv();
		
		if(recvMsg.equals(PROTOCOL.USER_BUS_RESERVATION_CONFIRM_SUCCESS)) {
			return true;
		}else {
			return false;
		}
	}
	
	public static void cancelBus() {
		String sendMsg = PROTOCOL.USER_BUS_CANCEL;
		send(sendMsg);
	}
	
	public static boolean waitVIBE() {
		String recvMsg = recv();
		if(recvMsg.equals(PROTOCOL.USER_BUS_ARRIVED_VIBE)) {
			return true;
		}else if(recvMsg.equals(PROTOCOL.USER_BUS_CANCEL_SUCCESS)) {
			return false;
		}else {
			return false;
		}
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
	
	// Please Fill methods below
	
	public static void setUserName(String name) {
		userName = name;
	}
	
	public static void setUserPhone(String phone) {
		userPhone = phone;
	}
	
	public static void setUserUID(String UID) {
		userUID = UID;
	}
	
	public static void setUserLati(double __lati) {
		_lati = __lati;
	}
	
	public static void setUserLong(double __long) {
		_long = __long;
	}
	
	public static String getUserName() {
		return userName;
	}
	
	public static String getUserPhone() {
		return userPhone;
	}
	
	public static String getUserUID() {
		return userUID;
	}
	
	public static double getUserLati() {
		return _lati;
	}
	
	public static double getUserLong() {
		return _long;
	}

	
}
