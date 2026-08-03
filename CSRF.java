if ("POST".equals(request.getMethod())) {
    String toAccount = request.getParameter("toAccount");
    String amount = request.getParameter("amount");
    transferMoney(toAccount, amount);
}
