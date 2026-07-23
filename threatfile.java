import java.util.List;

class PullRequest {
    String author;
    List<String> changedFiles;
    String commitMessage;

    public PullRequest(String author, List<String> changedFiles, String commitMessage) {
        this.author = author;
        this.changedFiles = changedFiles;
        this.commitMessage = commitMessage;
    }
}

class ThreatVerifier {
    public static boolean verifyPR(PullRequest pr) {
        // Rule 1: Block suspicious authors
        if (pr.author.equalsIgnoreCase("unknown") || pr.author.contains("bot")) {
            System.out.println("Threat detected: Suspicious author");
            return false;
        }

        // Rule 2: Check for sensitive file changes
        for (String file : pr.changedFiles) {
            if (file.contains("config") || file.contains("secrets") || file.contains("password")) {
                System.out.println("Threat detected: Sensitive file modification");
                return false;
            }
        }

        // Rule 3: Commit message sanity check
        if (pr.commitMessage == null || pr.commitMessage.trim().isEmpty()) {
            System.out.println("Threat detected: Empty commit message");
            return false;
        }
        if (pr.commitMessage.toLowerCase().contains("hack") || pr.commitMessage.toLowerCase().contains("exploit")) {
            System.out.println("Threat detected: Suspicious commit message");
            return false;
        }

        System.out.println("PR verified: No threats found");
        return true;
    }

    public static void main(String[] args) {
        PullRequest pr = new PullRequest(
            "akarshvidyarthi10",
            List.of("src/Main.java", "config/app.properties"),
            "Updated configuration"
        );

        boolean safe = verifyPR(pr);
        System.out.println("Verification result: " + safe);
    }
}
