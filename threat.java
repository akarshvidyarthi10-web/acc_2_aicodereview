// Vulnerable: no CSRF token check
if ("POST".equals(request.getMethod())) {
    String toAccount = request.getParameter("toAccount");
    String amount = request.getParameter("amount");
    transferMoney(toAccount, amount);
}
// Vulnerable: user can access any account by changing ID
String accountId = request.getParameter("accountId");
Account account = accountService.getAccount(accountId);

// Vulnerable: directly including user-specified file
String page = request.getParameter("page");
RequestDispatcher rd = request.getRequestDispatcher("/pages/" + page);
rd.forward(request, response);
