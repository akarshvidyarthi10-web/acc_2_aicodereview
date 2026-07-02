// Servlet example
protected void doGet(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {
    String comment = request.getParameter("comment"); // user input
    PrintWriter out = response.getWriter();

    // ❌ Directly printing user input without escaping
    out.println("<html><body>");
    out.println("User comment: " + comment); 
    out.println("</body></html>");
}
