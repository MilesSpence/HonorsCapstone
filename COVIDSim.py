#!/usr/bin/env python
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from createProbs import avg_infect_rate, avg_mort_rate, total_cases

# This is the most important of the simulations. It is for simulating the number of new cases,
# deaths, and vaccinations.

# Inputs.
N = 331002647
print("Total Population           =   "+ str(N))
Io = 886486
print("Infected population        =   " + str(Io));
Ro = 1863487
Do = 32045113
Vo = 93078040
print("Removed population         =   " + str(Ro));
So = N-Io-Ro-Vo
print("Susceptible population     =   " + str(So));

infection_rate = float(avg_infect_rate)

r = infection_rate*.9

y = 1/14
u = float(avg_mort_rate)

t = np.linspace(0, 100, 101)

# For an instant change in contact rate/stringency.
def change_contact(time):
    return 3 if time > 30 else .9

k = .5

# For a logarithmic change in contact rate/stringency.
def logistic_change(t):
    return (.9-1.5) / (1 + np.exp(-k*(-t+30))) + 1.5

# Assigns the contact rate.
def newBeta(time):
    return logistic_change(time) * infection_rate    
    #return r
    #return change_contact(time) * infection_rate

# This function is the actual mathematical model.
def sirdsv(y, t, N, beta, gamma, alpha, rho, m, q, z, special):
    S, I, R, D, V, special = y
    dSdt = (-newBeta(t) * S * I / N) + (m*R) - (z*q*S)
    dIdt = (newBeta(t) * S * I / N) - (1 - alpha)*gamma*I - alpha*rho*I
    dRdt = ((1 - alpha) * gamma * I) - (m*R)
    dDdt = alpha * rho * I
    dVdt = z*q*S
    special = newBeta(t) * S * I / N
    return dSdt, dIdt, dRdt, dDdt, dVdt, special

special = 0

initials = So, Io, Ro, Do, Vo, special
ret = odeint(sirdsv, initials, t, args=(N, r, y, u, 1/10, 1/30, 1/19, 1/14, 0))
S, I, R, D, V, special = ret.T


print("---------------------------------")

print("New cases:   " + str(special[len(special)-1]))
print("Total cases: " + str(total_cases+special[len(special)-1]))

print("Newly deceased people: " + str(D[len(D)-1]-Do))
print("Total deceased people: " + str(D[len(D)-1]))

print("Newly vaccinated people: " + str(V[len(V)-1]-Vo))
print("Total vaccinated people: " + str(V[len(V)-1]))



# Plotting the data.
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R, 'g', alpha=0.5, lw=2, label='Temporary Immunity')
ax.plot(t, D, 'k', alpha=0.5, lw=2, label='Deceased')
ax.plot(t, V, 'c', alpha=0.5, lw=2, label='Vaccinated')
ax.set_xlabel('Time (days)')
ax.set_ylabel('Millions')
ax.set_ylim(0,3000000)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.savefig('covidgraphzoomed.png')
plt.show()

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(t, S/100, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I/100, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R/100, 'g', alpha=0.5, lw=2, label='Temporary Immunity')
ax.plot(t, D/100, 'k', alpha=0.5, lw=2, label='Deceased')
ax.plot(t, V/100, 'c', alpha=0.5, lw=2, label='Vaccinated')
ax.set_xlabel('Time (days)')
ax.set_ylabel('Hundred millions')
ax.set_ylim(0,3000000)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.savefig('covidgraphfull.png')
plt.show()


choice = input("Would you like to email the results? ")

# For emailing the results of a simulation.
if(choice.lower() == "y" or choice.lower() == "yes"):
    import email, smtplib, ssl

    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    subject = "Covid Simulation"    
    body = "New cases:   " + str(special[len(special)-1]) + "\nTotal cases: " + str(total_cases+special[len(special)-1]) + "\n\nNewly deceased people: " + str(D[len(D)-1]-Do) + "\nTotal deceased people: " + str(D[len(D)-1]) + "\n\nNewly vaccinated people: " + str(V[len(V)-1]-Vo) + "\nTotal vaccinated people: " + str(V[len(V)-1])
    sender_email = "honorscapstone2021@gmail.com"
    receiver_email = input("Type your email address and press enter: ")
    password = input("Type your password and press enter: ")
    
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    
    filename = "covidgraphzoomed.png"  # In same directory as script
    filename2 = "covidgraphfull.png"
    
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    
    with open(filename2, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    print("\nSuccess! Check your inbox!")
    
