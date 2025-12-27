from fastapi import FastAPI
import uvicorn

app = FastAPI()

# Tool 1: Order Status
@app.get("/order/{order_id}")
def get_order_status(order_id: str):
    # Mock database
    mock_orders = {
        "ORD-123": {"status": "Shipped", "delivery_date": "2025-12-26"},
        "ORD-456": {"status": "Processing", "delivery_date": "TBD"},
        "ORD-999": {"status": "Cancelled", "refund_status": "Processed"}
    }
    
    result = mock_orders.get(order_id)
    if result:
        return result
    return {"status": "Not Found", "message": "Order ID does not exist."}

# Assignment 2: Ticket Creation Tool (Added here for efficiency)
@app.post("/create_ticket")
def create_support_ticket(user_issue: dict):
    # In a real app, this would save to a DB or Jira
    ticket_id = f"TICKET-{len(user_issue['description'])}"
    return {"ticket_id": ticket_id, "status": "Created", "priority": "High"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)