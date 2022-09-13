package oss;

public class BusArrival {
	
	private String routeNo;
	private int arrivalLeftNode;
	
	public BusArrival(String routeNo, int arrivalLeftNode) {
		this.routeNo = routeNo;
		this.arrivalLeftNode = arrivalLeftNode;
	}
	
	public String getRouteNo() {
		return this.routeNo;
	}
	
	public int arrivalLeftNode() {
		return this.arrivalLeftNode;
	}
	
}
