#---------------------------------------
# Import Libraries
#---------------------------------------
import bisect
import sys
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#---------------------------------------
# Script Information
#---------------------------------------

ScriptName = "bossMode"
Website = ""
Creator = "Fyruz_ & BidGem"
Version = "1.0.0"
Description = "Fight bosses to gain points"

#---------------------------------------
# Global Variables
#---------------------------------------

#a -> all

a_Boost = 0 #attack increment
a_BoostedAttack = 0 #boosted attack left

#b -> boss

b_CurrentBoss = 0
b_Name = 0
b_Health = 0
b_Damage = 0

#c -> command

c_AttackCommand = "!attacco"
c_SuperAttackCommand = "!superattacco"
c_lootsBotName = "loots_bot"
c_reviveCommand = "!rianima"
c_reviveMeCommand = "!rianimami"
#u -> user

u_SessionUser = []
u_SessionReviveList = []
u_SwordOwners = []

#v -> general variables

v_UserMatrix = [] #loaded from file
v_needWhisper = True #change to set bot chat type
v_ScriptName = "bossMode" #needed to set cooldown

#m -> message

m_SuperattackErrorSmems = "Devi inserire anche la quantità di SMEMS da voler usare"
m_SuperattackErrorCooldow = "Il super attacco si sta ricaricando, dei aspettare ancora "
m_AttackCooldown = "Ti devi riposare per ancora "
m_SuperAttack = " ha superattaccato e ha fatto "
m_reviveMeMessageNotEnoughPoints = "Hai messo un numero di SMEMS maggiore dei tuoi attuali SMEMS, metti una quantità minore di SMEMS per farti rianimare!"
m_reviveMessageCooldown = "Per poter rianimare qualcuno devi attendere ancora "
m_reviveMessageNotDead = "Questo player non è ancora morto, non puoi rianimarlo!"
m_reviveMeNotDead = "Sei ancora vivo, torna a combattere!"
m_reviveMeCorrect = "Adesso qualcuno può rianimarti! (Revime i've raygun)"


#---------------------------------------
# Initialize Data on Load
#---------------------------------------

def Init():

    getUsersFromFile()
    getBossFromFile()
    
    return
    
#---------------------------------------
#   Script is going to be unloaded
#---------------------------------------

def Unload():
    
	storeUsersInFile():
	storeBossInFile(): 
	
    return
    
#---------------------------------------
# Execute data and process messages
#---------------------------------------

def Execute(data):
        
    if(v_needWhisper):
        executeWithWisper(data)
    else:
        executeWithoutWisper(data)
        
    return    
#---------------------------------------
# Main function using normal messages
#---------------------------------------

def executeWithoutWisper(data):
        
    return  

#---------------------------------------
# Main function using whisper
#---------------------------------------

def executeWithWisper(data):

	global a_Boost #calling global vars
	global b_Health
	global a_BoostedAttack
  	 
    userMainIndex = searchAddUser([data.User,100], u_SessionUser) #-> TODO ADD USER TO SESSION, CHECK PRSENCE BEFORE (FUNCT NEED TO BE CREATED)
    
    if(data.User == c_lootsBotName): #incoming loots message
	
		updateBoost()
    
    elif(data.GetParam(0) == c_AttackCommand): #attack command
		if(!isCooldown(data.User, c_AttackCommand)):
			
			attackBoss(data)
			
		else:
               
			sendWhisper(data.User, m_AttackCooldown + getCoolDown(data.User, c_AttackCommand) + " secondi") #send whisper if A is on cooldown
            
		elif(data.GetParam(0) == c_SuperAttackCommand): #superattack command
			if(!isCooldown(cdata.User, c_SuperAttackCommand)): 
				if(int(data.GetParam(1)) <= Parent.GetPoints(data.User)): #check if user send an amount of points to use superattack
            
					superAttackBoss(data)
				
				else: 
					sendWhisper(data.User, m_SuperattackErrorSmems) #send whisper if SA is missing points
						
				else:
					sendWhisper(data.User, m_SuperattackErrorCooldown + getCoolDown(data.User, c_AttackCommand) + " secondi") #send whisper if SA is on cooldown
			
        elif(data.GetParam(0) == c_reviveCommand):
			if(!isCooldown(data.User, c_reviveCommand)):
				if((revIndex = searchUser(data.GetParam(1), u_SessionReviveList)) > -1): 
              
					revive(data, revIndex)
              
				else:
                
					sendWhisper(data.User, m_reviveMessageNotDead)
              
			else:
				sendWhisper(data.User, m_reviveMessageCooldown + getCoolDown(data.User, c_reviveCommand) + "secondi")
        elif(data.GetParam(0) == c_reviveMeCommand):
          
			userIndex = searchUser(data.User, u_SessionUser)
          
          	if(u_SessionUser[userIndex][1] <= 0)
            	if(data.GetParam(1) <= Parent.GetPoints(data.User)):
            
            	 	index = searchUser(data.User, u_SessionReviveList)
            		u_SessionReviveList[index][1] = data.GetParam(1)
					if(data.GetParam(1) >= u_SessionReviveList[index][1] )
						Parent.RemovePoints(data.User, data.GetParam(1) - u_SessionReviveList[index][1]) #TODO in unload readd points to non revived users, check if user already ask to revive to avoid point loosing
						u_SessionReviveList[index][1] = data.GetParam(1)
					sendWhisper(data.User, m_reviveMeCorrect)
                
				else:
					sendWhisper(data.User, m_reviveMeMessageNotEnoughPoints)
            
			else:
				sendWhisper(data.User, m_reviveMeNotDead)
            
    return  

#---------------------------------------
# Used to revive someone
#---------------------------------------
  
def revive(data, revIndex):
  
	userToRevive = u_SessionReviveList[revIndex][0] #USED TO REMOVE POINTS
	userIndex = searchUser(userToRevive, u_SessionUser) #USED TO ADD LIFE
	u_SessionUser[userIndex][1] = 100 #GIVE HEALTH TO THE USER TO REVIVE
	pointsToGive = u_SessionReviveList[revIndex][1] #GET POINTS NUMBER
	Parent.AddPoints(data.User, pointsToGive) #ADD POINTS TO HEALER #TODO 
	u_SessioReviveList.remove(revIndex) #REMOVE USER FROM REVIVE LIST
  
	return
  
#---------------------------------------
# Used to attack Boss
#---------------------------------------

def attackBoss(data):
  
	global a_Boost #calling global vars
	global b_Health
	global a_BoostedAttack
  
	u_BoostedAttack = 0
	u_Attack = (10 + (5 * data.GetHours()))
		if(a_BoostedAttack > 0): #check if there are boosted attack left
			u_BoostedAttack = u_Attack * a_Boost / 100
			a_BoostedAttack = a_BoostedAttack - 1
			b_Health = b_Health - (u_Attack + u_BoostedAttack)
	addCooldown(data.User, c_AttackCommand, 30)
  
	return

#---------------------------------------
# Used to super-attack Boos
#---------------------------------------
  
def superAttack(data):
  
	global a_Boost #calling global vars
	global b_Health
	global a_BoostedAttack
  
	u_BoostedAttack = 0
	u_PointBoost = Parent.GetPoints(data.User)
	u_Attack = int(10 + 5 * data.GetHours() + ( 10 + 5 * data.GetHours()) * u_PointBoost / 100)
	if(a_BoostedAttack > 0): #check if there are boosted attack left
		u_BoostedAttack = u_Attack * a_Boost / 100
		a_BoostedAttack = a_BoostedAttack - 1
	b_Health = b_Health - (u_Attack + u_BoostedAttack)
	Parent.RemovePoints(data.User, int(data.GetParam(1)))
	addCooldown(data.User, c_SuperAttackCommand, 300)
	sendMessage(GetDisplayName(data.user) + m_SuperAttack + u_BoostedAttack + " danni !!")
  
	return
  
#---------------------------------------
# Update boosts values
#---------------------------------------
	
def updateBoost():

	global a_Boost
	global a_BoostedAttack
	
	if(a_BoostedAttack <= 0):
		a_BoostedAttack = 10
    else:
		a_BoostedAttack = a_BoostedAttack + 1
		a_Boost = a_Boost + 5

	return	
	
	
#---------------------------------------
# [Integer] Get user cooldown for a specified command
#---------------------------------------
	
def getCoolDown(user, command): #get user cooldown for a specified command

	return Parent.GetUserCooldownDuration(v_ScriptName, command, user)
	
#---------------------------------------
# [Boolean] Get user cooldown for a specified command
#---------------------------------------
	
def isCooldown(user, command):

	return Parent.IsOnUserCooldown(v_ScriptName, command, user)
	
#---------------------------------------
# Add user cooldown for a specified command
#---------------------------------------
	
def addCooldown(user, command, time):

	Parent.AddUserCooldown(bossMode, command, user, time)

	return
	
#---------------------------------------
# Send a whisper to a specified user
#---------------------------------------	
	
def sendWhisper(user, message):

	Parent.SendTwitchWhisper(user, message)

	return
	
#---------------------------------------
# Send a twitch chat message
#---------------------------------------		

def sendMessage(message):

	Parent.SendTwitchMessage(message)
	
	return
    
#---------------------------------------
# Obtain all players from file
#---------------------------------------

def getUsersFromFile():
    """
    read users.txt and put the informations in v_UserMatrix. users.txt must have this format:
    
    userName,damageInflicted,otherOptionalFields
    userName,damageInflicted,otherOptionalFields
    [...]
    
    """
    
    global v_UserMatrix
    usersFile = open("users.txt", "r")
    temp_data = usersFile.readlines()
   
    for line in temp_data:        
    
        words = line.split(",")
        words[1] = int(words[1])
        v_UserMatrix.append(words)

    usersFile.close()
    return
  
#---------------------------------------
# Obtain sword owners from file:
#---------------------------------------

def getSwordOwnersFromFile():
    """
    read sword.txt and put the informations in u_SwordOwners. sword.txt must have this format:
    Username,Username,Username,[...]    
    """
    
    global u_SwordOwners
    inFile = open("sword.txt", "r")
    temp_data = inFile.read()
   	u_SwordOwners = temp_data.split(",")
    inFile.close()
    return
    
#---------------------------------------
# Obtain boss attributes from file
#---------------------------------------
    
def getBossFromFile():
    """
    read boss.txt and load the information of the current boss. Put them in b_
    boss.txt must have this format:
    
    currentBoss_Index
    bossIndex,bossName,bossHealth,bossDamage
    bossIndex,bossName,bossHealth,bossDamage
    [...]
    
    """
    global b_CurrentBoss
    global b_Name
    global b_Health
    global b_Damage
    
    bossFile = open("boss.txt", "r")
    str_b_CurrentBoss = bossFile.readline()
    b_CurrentBoss = int(str_b_CurrentBoss.split(",")[0])
    for line in bossFile:
        words = line.split(",")
        index = words[0]
        if (int(index) == b_CurrentBoss):
            b_Name = words[1]
            b_Health = words[2]
            b_Damage = words[3]
            bossFile.close()
            break
        
    return
            
#---------------------------------------
#Store players matrix to file
#---------------------------------------

def storeUsersInFile():

    global v_UserMatrix
    
    userFile = open("users.txt", "w")
    for i in v_UserMatrix:
        dataline = (v_UserMatrix[0][0] + "," + str(v_UserMatrix[0][1]))
        userFile.write(dataline + "\n")
    
    userFile.close()
    return

  
#---------------------------------------
#Store sword matrix to file
#---------------------------------------

def storeSwordOwnersInFile():

    global u_SwordOwners
    
    outFile = open("sword.txt", "w")
    for i in u_SwordOwners:
        dataline = (i + ",")
        outFile.write(dataline)
    
    outFile.close()
    return  
  
  
#-----------------------------
#If b_Defeated then update boss.txt 
#-----------------------------

def storeBossInFile(): 
    global b_CurrentBoss
    global b_Defeated
    
    if b_Defeated:
        outFile = open("boss.txt","r+")
        outFile.write(str(b_CurrentBoss+1)+",")
        outFile.close()
    
    return


#-----------------------------
#if the user own a sword return 1.3, else return 1
#-----------------------------

def swordMultiplier(user):
  global u_SwordOwnsers
  i = 0
  while i<len(u_SwordOwners) and user != u_SwordOwners[0]:
    i = i+1;
    
  if i<len(u_SwordOwners):
    return 1.3
  else:
    return 1
  
  
#-----------------------------
#search an user in a list and return the index.
#If the user isn't in the list, add it kepping the list sorted, then return the index.
#u must be a list. If u has a second element and alist contains e, with e[0] == u[0] and 
#search -> O(log(n))
#insertion -> O(n)
#-----------------------------
       
def searchAddUser(u, alist):
    i = bisect.bisect(alist, u)
    if i < len(alist) and alist[i][0] == u[0]:
        return i
    
    elif alist[i-1][0] == u[0]:
        return i-1
    
    else:
        alist.insert(i, u)
        return i
      
#-----------------------------
#search an user in a list and return the index.
#-----------------------------
      
def searchUser(u, alist):
    i = bisect_left(alist, u)
    if i != len(a) and a[i] == x:
        return i
    else:
      	return -1