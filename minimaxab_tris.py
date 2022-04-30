import time
import numpy as np
from math import inf as infinity

Utente = -1
Engine = +1
grid = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def vittoria(stato, giocatore):
    '''
    funzione che controlla chi ha vinto

    Parametri
    ---------
    stato : list
        matrice del campo da gioco
    giocatore : int
        assume valori +-1 a seconda di chi gioca

    Return
    ---------
    Bolean True se giocatore ha vinto False altrimenti
    '''
    #casistiche possibili
    stato_vincente = [
        [stato[0][0], stato[0][1], stato[0][2]],  #righe
        [stato[1][0], stato[1][1], stato[1][2]],
        [stato[2][0], stato[2][1], stato[2][2]],
        [stato[0][0], stato[1][0], stato[2][0]],  #colonne
        [stato[0][1], stato[1][1], stato[2][1]],
        [stato[0][2], stato[1][2], stato[2][2]],
        [stato[0][0], stato[1][1], stato[2][2]],  #diagonali
        [stato[2][0], stato[1][1], stato[0][2]],
    ]
    #controllo
    if [giocatore]*3 in stato_vincente:
        return True
    else:
        return False

def game_over(stato):
    '''
    ritorna True se la partita è finita

    Parametri
    ---------
    stato : list
        matrice del campo da gioco

    Return
    ---------
    Bolean True se uno dei giocatori ha vinto False altrimenti
    '''
    return vittoria(stato, Utente) or vittoria(stato, Engine)

def libero(stato):
    '''
    controlla le caselle libere

    Parametri
    ---------
    stato : list
        matrice del campo da gioco

    Return
    ---------
    celle : list
        lista delle coordinate delle celle vuote
    '''
    celle = []

    for x, riga in enumerate(stato):
        for y, cella in enumerate(riga):
            if cella == 0:
                celle.append([x, y])

    return celle

def mossa_valida(x, y):
    '''
    controlla la validità della mossa
    la mossa deve essere nelle caselle libere

    Parametri
    ---------
    x, y : int
        indici della matrice del campo da gioco

    Return
    ---------
    Bolean True se x e y sono indici di una casella vuota False altrimenti
    '''
    if [x, y] in libero(grid):
        return True
    else:
        return False


def mossa(x, y, giocatore):
    '''
    esegue la mossa se valida la cella
    assume valore +-1 a seconda del giocatore

    Parametri
    ---------
    x, y : int
        indici della matrice del campo da gioco
    giocatore : int
        assume valori +-1 a seconda di chi gioca

    Return
    ---------
    Bolean True se la mossa è stata eseguita false altrimenti
    '''
    if mossa_valida(x, y):
        grid[x][y] = giocatore
        return True
    else:
        return False

def stampa(stato, c_s, u_s):
    '''
    stampa a schermo la griglia

    Parametri
    ---------
    stato : list
        matrice del campo da gioco
    c_s : string
        stringa che contiene il simbolo del computer
    u_s : string
        stringa che contiene il simbolo dell' utente
    '''
    #dizionario per far diventarre i +-1 in x e o
    chars = {-1: u_s, +1: c_s, 0: ' '}

    line = '---------------'
    print('\n' + line)

    for riga in stato:
        for cella in riga:
            simbolo = chars[cella]
            print(f'| {simbolo} |', end='')
        print('\n' + line)

def turno_utente(c_s, u_s):
    '''
    mossa utente

    Parametri
    ---------
    c_s : string
        stringa che contiene il simbolo del computer
    u_s : string
        stringa che contiene il simbolo dell' utente
    '''
    #controllo fine gioco
    depth = len(libero(grid))
    if depth == 0 or game_over(grid):
        return
    #possibili entrate della griglia che è 3x3
    posizione = {
        7: [0, 0], 8: [0, 1], 9: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        1: [2, 0], 2: [2, 1], 3: [2, 2],
    }

    print(f'turno utente [{u_s}]')
    stampa(grid, c_s, u_s)

    while True:
        while True:
            pos = int(input('usa numeri da 1 a 9: '))
            if not pos in [1,2,3,4,5,6,7,8,9]:
                print('mossa invalida, puoi ritentare')
            else:
                break
        coord = posizione[pos]
        Mossa = mossa(coord[0], coord[1], Utente)
        if not Mossa:
            print('mossa invalida, puoi ritentare')
        else:
            break

def punti(stato):
    '''
    conteggio punti, necessario per minimax
    per vedre se le mosse del computer sono vincenti

    Parametri
    ---------
    stato : list
        matrice del campo da gioco

    Return
    ---------
    punteggio : int
        1 se il computer vinche, -1 se perde, 0 per pareggio
    '''
    if vittoria(stato, Engine):
        punteggio = +1
    elif vittoria(stato, Utente):
        punteggio = -1
    else:
        punteggio = 0

    return punteggio


def minimax(stato, depth, giocatore):
    '''
    algoritmo gioco computer

    Parametri
    ---------
    stato : list
        matrice del campo da gioco
    depth : int
        quante caselle libere ci sono, quindi quanto andare
        in frofondità con le possibili partite
    giocatore : int
        assume valori +-1 a seconda di chi gioca

    Return
    ---------
    best : list
        [x migliore, y migliore, miglior punteggio]
    '''
    def maxplayer(stato, depth, giocatore):

        best = [-1, -1, -infinity]

        #controllo fine gioco
        if depth == 0 or game_over(stato):
            punteggio = punti(stato)
            return [-1, -1, punteggio]

        for cella in libero(stato):
            x, y = cella[0], cella[1]
            stato[x][y] = giocatore
            punteggio = minplayer(stato, depth-1, -giocatore)
            stato[x][y] = 0
            punteggio[0], punteggio[1] = x, y
            if punteggio[2] > best[2]:
                best = punteggio
            if punteggio[2] == 1:
                break
        return best

    def minplayer(stato, depth, giocatore):

        best = [-1, -1, +infinity]

        #controllo fine gioco
        if depth == 0 or game_over(stato):
            punteggio = punti(stato)
            return [-1, -1, punteggio]

        for cella in libero(stato):
            x, y = cella[0], cella[1]
            stato[x][y] = giocatore
            punteggio = maxplayer(stato, depth-1, -giocatore)
            stato[x][y] = 0
            punteggio[0], punteggio[1] = x, y
            if punteggio[2] < best[2]:
                best = punteggio
            if punteggio[2] == -1:
                break
        return best

    if giocatore == Engine:
        return maxplayer(stato, depth, giocatore)
    else:
        return minplayer(stato, depth, -giocatore)

def turno_computer(c_s, u_s):
    '''
    mossa computer

    Parametri
    ---------
    c_s : string
        stringa che contiene il simbolo del computer
    u_s : string
        stringa che contiene il simbolo dell' utente
    '''
    #controllo fine gioco
    depth = len(libero(grid))
    if depth == 0 or game_over(grid):
        return

    print(f'turno computer[{c_s}]')
    stampa(grid, c_s, u_s)

    #prima mossa del computer è casuale
    if depth == 9:
        x = np.random.randint(3)
        y = np.random.randint(3)
    else:

        move = minimax(grid, depth, Engine)
        x, y = move[0], move[1]
    mossa(x, y, Engine)


def main():
    '''
    funzione che avvia il gioco
    '''
    #simboli
    u_s = ''
    c_s = ''
    #chi inizia
    first = ''
    print('Gioca a tris contro il computer')
    while True:
        u_s = input('scegli  x oppure o \nscegli: ')
        if u_s != 'x' and u_s != 'o':
            print('carattere non valido, riscesgli (è case sensitive)')
        else:
            break
    if u_s == 'x':
        c_s = 'o'
    else:
        c_s = 'x'

    while True:
        first = input('Giocare per primo?[y/n]: ')
        if first != 'y' and first != 'n':
            print('carattere non valido, è case sensitive')
        else:
            break

    print('\nACHTUNG: le caselle sono ordinate come nel tastierino \n')
    while len(libero(grid)) > 0 and not game_over(grid):
        if first == 'n':
            turno_computer(c_s, u_s)
            first = '' #in modo che ip computer non faccia due turni

        turno_utente(c_s, u_s)
        turno_computer(c_s, u_s)


    if vittoria(grid, Utente):

        print(f'turno utente [{u_s}]')
        stampa(grid, c_s, u_s)
        print('Complimenti, hai vinto!')

    elif vittoria(grid, Engine):

        print(f'turno computer [{c_s}]')
        stampa(grid, c_s, u_s)
        print('Mi spiace, hai perso')
        print('F')

    else:

        stampa(grid, c_s, u_s)
        print('Pareggio')

main()
