import 'package:flutter/material.dart';
import 'profile_screen.dart';
import 'widget.dart';
import '../constants.dart';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';

class HomeScreen extends StatelessWidget {
  final int userId;
  const HomeScreen({super.key, required this.userId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF3F6FF),
      appBar: AppBar(
        elevation: 0,
        title: const Text("Dashboard"),
        backgroundColor: Colors.deepPurple,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: GridView.count(
          crossAxisCount: 2,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
          children: [
            GradientMenuCard(
              icon: Icons.upload_file,
              title: "Upload",
              onTap: () => uploadNote(context),
            ),
            GradientMenuCard(
              icon: Icons.download,
              title: "Download",
              onTap: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("Download feature coming soon")),
                );
              },
            ),
            GradientMenuCard(
              icon: Icons.search,
              title: "Search",
              onTap: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("Search feature coming soon")),
                );
              },
            ),
            GradientMenuCard(
              icon: Icons.person,
              title: "Profile",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => ProfileScreen(userId: userId)),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Future<void> uploadNote(BuildContext context) async {
    final result = await FilePicker.platform.pickFiles();
    if (result != null) {
      final file = result.files.first;
      var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/upload'));
      request.files.add(await http.MultipartFile.fromPath('file', file.path!));
      var response = await request.send();
      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("File uploaded successfully")),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Upload failed")),
        );
      }
    }
  }
}
