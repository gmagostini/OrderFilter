



with open("ciao.html" , mode='w') as file_out:
    file_out.write("""
        <table border=1>
            <tr>
                <th>Number</th>
                <th>Square</th>
            </tr>
        <indent>
        <% for i in range(10): %>
            <tr>
                <td><%= i %></td>
                <td><%= i**2 %></td>
            </tr>
        </indent>
        </table>
          """)