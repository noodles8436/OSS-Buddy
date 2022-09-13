package ossUser;

import java.util.ArrayList;

import ossBusDriver.NetworkBus;

public class Main {

	public static void main(String[] args) throws InterruptedException {
		busDriverClient();
		userClient();
	}
	
	public static void userClient() throws InterruptedException {
		Network.start();
		
		Network.setUserName("도뚝딱");
		Network.setUserPhone("01045785678");
		Network.setUserUID("ASFJHFIUAE");
		
		System.out.println("Register : " + Network.register());
		Thread.sleep(1000);
		System.out.println("Login : " + Network.login());
		System.out.println("Search Near Location : " + Network.readyforLocation());
		
		ArrayList<BusArrival> busList = Network.getBusList();
		if(busList.size() > 0) {
			BusArrival bus = busList.get(0);
			
			System.out.println("BUS : " + bus.getRouteNo() + 
					" | Arrival Left Node : " + bus.arrivalLeftNode());
			
			boolean isPossible = Network.isPossibleBus(bus.getRouteNo());
			
			
			if(isPossible) {
				System.out.println("Now " + bus.getRouteNo() + " can be reserved!");
				Thread.sleep(3000);
				System.out.println("Ready to Reserving");
				boolean isReserved = Network.reserveBus(bus.getRouteNo());
				
				if(isReserved) {
					System.out.println(bus.getRouteNo() + " BUS Reserved Successfully");
					if(Network.waitVIBE()) {
						System.out.println(bus.getRouteNo() + "VIBERATION!");
					}else {
						System.out.println("Cancelled..");
					}
				}else {
					System.out.println(bus.getRouteNo() + " BUS Reservation Failed");
				}
				
			}else {
				System.out.println("Now " + bus.getRouteNo() + " can NOT be reserved!");
			}
			
		}
		
		// Network.isPossibleBus(routeNo);
		
		// Network.reserveBus(routeNo);
		// Network.waitVIBE();
		// 종료 이후 화면 처리
		
		// Network.cancelBus();
	}
	
	public static void busDriverClient() {
		NetworkBus.setDriverName("홍기사");
		NetworkBus.setDriverVehicleNo("강원71자1322");
		NetworkBus.setDriverUID("ASDWQRTFHEI");
		NetworkBus.setDriverRouteNo("30");
		NetworkBus.start();
		
		NetworkBus.register();
		NetworkBus.login();
	}

}
