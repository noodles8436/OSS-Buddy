package oss;

import oss.Network;
import oss.BusArrival;
import java.util.ArrayList;

public class Main {

	public static void main(String[] args) {
		Network.start();
		Network.login();
		Network.readyforLocation();
		ArrayList<BusArrival> busList = Network.getBusList();
		for(BusArrival bus : busList) {
			System.out.println(bus.getRouteNo());
			System.out.println(bus.arrivalLeftNode());
		}
		// Network.isPossibleBus();
		// Network.reserveBus();
		// Network.waitVIBE();
		// Network.cancelBus();
	}

}
