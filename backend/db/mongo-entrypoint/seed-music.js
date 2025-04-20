// print('===============JAVASCRIPT===============');
// print('Count of rows in test collection: ' + db.test.count());

// db.test.insert({ myfield: 'test1', anotherfield: 'TEST1' });
// db.test.insert({ myfield: 'test2', anotherfield: 'TEST2' });

// print('===============AFTER JS INSERT==========');
// print('Count of rows in test collection: ' + db.test.count());

// alltest = db.test.find();
// while (alltest.hasNext()) {
//   printjson(alltest.next());
// }
// Kết nối đến database 'test'
db = db.getSiblingDB('test');

// Chèn dữ liệu TLS Pie vào collection 'tls_pie_data'
db.tls_pie_data.insertMany([
  { name: "TLS1.2", value: 23 },
  { name: "TLS1.3", value: 27 },
  { name: "TLS1.1", value: 18 },
  { name: "Old SSL", value: 32 }
]);

// Chèn trạng thái vào collection 'status_info'
db.status_info.insertOne({ current_status: "unsafe" }); // Hoặc "safe"

// Chèn dữ liệu Missed Bytes vào collection 'missed_bytes_data'
db.missed_bytes_data.insertMany([
  { time: "8:00", missed_bytes: 20 },
  { time: "8:15", missed_bytes: 55 },
  { time: "8:30", missed_bytes: 35 },
  { time: "8:45", missed_bytes: 30 }
]);

// Chèn dữ liệu Logs vào collection 'logs_data'
db.logs_data.insertMany([
  { protocol: "TLS1.2", status: "Safe" },
  { protocol: "Old SSL", status: "Unsafe" },
  { protocol: "TLS1.2", status: "Safe" },
  { protocol: "TLS1.2", status: "Safe" },
  { protocol: "TLS1.2", status: "Safe" },
  { protocol: "TLS1.2", status: "Safe" },
  { protocol: "TLS1.2", status: "Safe" }
]);

print("Dữ liệu đã được khởi tạo thành công!");