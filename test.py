import mcstatus

server = mcstatus.MinecraftServer('localhost',25565)

print(server.status())