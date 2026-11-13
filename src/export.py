import json
import csv
import os
import yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom
from src.database import get_connection

def get_joined_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            t.TicketID,
            t.statusPayment,
            t.start_date AS ticket_date,
            u.passengerID,
            u.name AS user_name,
            u.surname AS user_surname,
            tr.TripID,
            tr.name AS trip_name,
            tr.cost AS trip_cost,
            tr.start_date AS trip_start_date
        FROM Ticket t
        JOIN User u ON t.passengerID = u.passengerID
        JOIN Trip tr ON t.TripID = tr.TripID
    """)

    columns = [column[0] for column in cur.description]
    data = [dict(zip(columns, row)) for row in cur.fetchall()]
    conn.close()
    return data

def export_data():
    out_dir = "out"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    raw_data = get_joined_data()

    json_data = []
    for row in raw_data:
        json_data.append({
            "ticket_id": row["TicketID"],
            "status_payment": bool(row["statusPayment"]),
            "ticket_date": row["ticket_date"],
            "passenger": {
                "id": row["passengerID"],
                "full_name": f"{row['user_surname']} {row['user_name']}"
            },
            "trip": {
                "id": row["TripID"],
                "name": row["trip_name"],
                "cost": row["trip_cost"],
                "start_date": row["trip_start_date"]
            }
        })
    
    with open(os.path.join(out_dir, "data.json"), "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    csv_file = os.path.join(out_dir, "data.csv")
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["TicketID", "StatusPayment", "PassengerName", "TripName", "TripCost"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in raw_data:
            writer.writerow({
                "TicketID": row["TicketID"],
                "StatusPayment": row["statusPayment"],
                "PassengerName": f"{row['user_surname']} {row['user_name']}",
                "TripName": row["trip_name"],
                "TripCost": row["trip_cost"]
            })

    root = ET.Element("tickets")
    for row in raw_data:
        ticket_elem = ET.SubElement(root, "ticket", id=str(row["TicketID"]))
        
        ET.SubElement(ticket_elem, "statusPayment").text = str(row["statusPayment"])
        ET.SubElement(ticket_elem, "ticketDate").text = row["ticket_date"]
        
        passenger_elem = ET.SubElement(ticket_elem, "passenger")
        ET.SubElement(passenger_elem, "id").text = str(row["passengerID"])
        ET.SubElement(passenger_elem, "fullName").text = f"{row['user_surname']} {row['user_name']}"
        
        trip_elem = ET.SubElement(ticket_elem, "trip")
        ET.SubElement(trip_elem, "id").text = str(row["TripID"])
        ET.SubElement(trip_elem, "name").text = row["trip_name"]
        ET.SubElement(trip_elem, "cost").text = str(row["trip_cost"])
        ET.SubElement(trip_elem, "startDate").text = row["trip_start_date"]

    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    with open(os.path.join(out_dir, "data.xml"), "w", encoding="utf-8") as f:
        f.write(xml_str)

    yaml_data = []
    for row in raw_data:
        yaml_data.append({
            "ticket_id": row["TicketID"],
            "status_payment": bool(row["statusPayment"]),
            "passenger": {
                "id": row["passengerID"],
                "full_name": f"{row['user_surname']} {row['user_name']}"
            },
            "trip": {
                "id": row["TripID"],
                "name": row["trip_name"],
                "cost": row["trip_cost"]
            }
        })
    
    with open(os.path.join(out_dir, "data.yaml"), "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)

    print(f"Данные успешно экспортированы в папку '{out_dir}': data.json, data.csv, data.xml, data.yaml")

if __name__ == "__main__":
    export_data()