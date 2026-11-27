import json
import csv
import os
import yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom
from src.system.database import get_connection


def get_joined_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            t.TicketID       AS ticketID,
            t.statusPayment  AS statusPayment,
            t.TripID         AS ticket_trip_id,
            u.passengerID    AS passengerID,
            u.name           AS user_name,
            u.surname        AS user_surname,
            tr.name          AS trip_name,
            tr.cost          AS trip_cost,
            tr.start_date    AS trip_start_date
        FROM Ticket t
        JOIN User u ON t.passengerID = u.passengerID
        JOIN Trip tr ON t.TripID = tr.TripID
    """)
    columns = [c[0] for c in cur.description]
    data = [dict(zip(columns, row)) for row in cur.fetchall()]
    conn.close()
    return data


def export_data():
    out_dir = "out"
    os.makedirs(out_dir, exist_ok=True)

    raw_data = get_joined_data()

    json_data = []
    for row in raw_data:
        json_data.append({
            "ticket_id": row["ticketID"],
            "status_payment": bool(row["statusPayment"]),
            "passenger": {
                "id": row["passengerID"],
                "full_name": f"{row['user_surname']} {row['user_name']}"
            },
            "trip": {
                "id": row["ticket_trip_id"],
                "name": row["trip_name"],
                "cost": row["trip_cost"],
                "start_date": row["trip_start_date"]
            }
        })
    with open(os.path.join(out_dir, "data.json"), "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    with open(os.path.join(out_dir, "data.csv"), "w", encoding="utf-8", newline="") as f:
        fieldnames = ["TicketID", "StatusPayment", "PassengerName", "TripName", "TripCost"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in raw_data:
            writer.writerow({
                "TicketID": row["ticketID"],
                "StatusPayment": row["statusPayment"],
                "PassengerName": f"{row['user_surname']} {row['user_name']}",
                "TripName": row["trip_name"],
                "TripCost": row["trip_cost"]
            })

    root = ET.Element("tickets")
    for row in raw_data:
        ticket_elem = ET.SubElement(root, "ticket", id=str(row["ticketID"]))
        ET.SubElement(ticket_elem, "statusPayment").text = str(row["statusPayment"])
        passenger_elem = ET.SubElement(ticket_elem, "passenger")
        ET.SubElement(passenger_elem, "id").text = str(row["passengerID"])
        ET.SubElement(passenger_elem, "fullName").text = f"{row['user_surname']} {row['user_name']}"
        trip_elem = ET.SubElement(ticket_elem, "trip")
        ET.SubElement(trip_elem, "id").text = str(row["ticket_trip_id"])
        ET.SubElement(trip_elem, "name").text = row["trip_name"]
        ET.SubElement(trip_elem, "cost").text = str(row["trip_cost"])
        ET.SubElement(trip_elem, "startDate").text = row["trip_start_date"]

    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    with open(os.path.join(out_dir, "data.xml"), "w", encoding="utf-8") as f:
        f.write(xml_str)

    yaml_data = []
    for row in raw_data:
        yaml_data.append({
            "ticket_id": row["ticketID"],
            "status_payment": bool(row["statusPayment"]),
            "passenger": {
                "id": row["passengerID"],
                "full_name": f"{row['user_surname']} {row['user_name']}"
            },
            "trip": {
                "id": row["ticket_trip_id"],
                "name": row["trip_name"],
                "cost": row["trip_cost"]
            }
        })
    with open(os.path.join(out_dir, "data.yaml"), "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)

    print(f"Данные экспортированы в '{out_dir}': data.json, data.csv, data.xml, data.yaml")


if __name__ == "__main__":
    export_data()