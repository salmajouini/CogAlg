from collections import deque
import math as math
from time import time
import frame_blobs
from angle_blobs import comp_angle

'''
    intra_blob() is an extension to frame_blobs, it performs evaluation for comp_P and recursive frame_blobs within each blob.
    Currently it's mostly a draft, combined with frame_blobs it will form a 2D version of first-level algorithm
    inter_blob() will be second-level 2D algorithm, and a prototype for meta-level algorithm

    colors will be defined as color / sum-of-colors, color Ps are defined within sum_Ps: reflection object?
    relative colors may match across reflecting objects, forming color | lighting objects?     
    comp between color patterns within an object: segmentation?

    inter_olp_blob: scan alt_typ_ ) alt_color, rolp * mL > ave * max_L?   
    intra_blob rdn is eliminated by merging blobs, reduced by full inclusion: mediated access?
'''


def eval_blob(blob, dert__):  # evaluate blob for comp_angle, incr_rng_comp, incr_der_comp, comp_Py_, orthogonal blob flip

    s, [min_x, max_x, min_y, max_y, xD, abs_xD, Ly], [L, I, G, Dx, Dy, abs_Dx, abs_Dy], root_ = blob
    Ave = ave * L  # whole-blob reprocessing filter, fixed: no if L?
    rdn = 1  # redundant representation counter
    val_deriv, val_range = 0, 0

    if s:  # positive blob, primary orientation match eval: noisy or directional gradient
        if G > Ave:  # likely edge, ave d_angle = ave g?
            rdn += 1  # or greater?
            comp_angle(blob, dert__)  # angle comparison, ablob definition; A, sDa accumulation in aP, aseg, ablob, blob
            sDa = blob[2][7]

            val_deriv = G * -sDa  # -sDa indicates proximate angle match -> recursive comp(d_): dderived?
        val_range = G  # G without angle is not directional, thus likely d reversal and match among distant pixels
    val_comp_Py_ = L + I + G + Dx + Dy  # max P match, also abs_Dx, abs_Dy: more accurate but not needed for most blobs?

    values = val_deriv, val_range, val_comp_Py_
    c, b, a = sorted(values)
    # three instances of generic evaluation for three branches of recursion:

    if a > Ave * rdn:  # filter adjusted for redundancy to previously formed representations
        rdn += 1
        if a is val_range:
            inc_range(blob, rdn)  # recursive comp over p_ of incremental distance, also diagonal?
        elif a is val_deriv:
            inc_deriv(blob, rdn)  # recursive comp over d_ of incremental derivation
        else:
            comp_Py_(val_comp_Py_, 0, blob, xD, rdn)  # leading to comp_P

        if b > Ave * rdn:  # filter adjusted for redundancy to previously formed representations
            rdn += 1
            if b is val_range:
                inc_range(blob, rdn)  # recursive comp over p_ of incremental distance, also diagonal?
            elif b is val_deriv:
                inc_deriv(blob, rdn)  # recursive comp over d_ of incremental derivation
            else:
                comp_Py_(val_comp_Py_, 0, blob, xD, rdn)  # leading to comp_P

            if c > Ave * rdn:  # filter adjusted for redundancy to previously formed representations
                rdn += 1
                if c is val_range:
                    inc_range(blob, rdn)  # recursive comp over p_ of incremental distance, also diagonal?
                elif c is val_deriv:
                    inc_deriv(blob, rdn)  # recursive comp over d_ of incremental derivation
                else:
                    comp_Py_(val_comp_Py_, 0, blob, xD, rdn)  # leading to comp_P

    return blob


# everything below is a draft

def inc_range(blob, rdn):  # frame_blobs recursion if sG
    return blob


def inc_deriv(blob, rdn):  # frame_blobs recursion if Dx + Dy: separately, or abs_Dx + abs_Dy: directional, but for both?
    return blob


def flip(blob, rdn):  # vertical-first run of form_P and deeper functions over blob's ders__
    return blob


def comp_Py_(val_comp_Py_, norm, blob, xD, rdn):  # scan of vertical Py_ -> comp_P -> 2D mPPs and dPPs
    s, [min_x, max_x, min_y, max_y, xD, abs_xD, Ly], [L, I, G, Dx, Dy, abs_Dx, abs_Dy], root_ = blob

    if val_comp_Py_ * ((max_x - min_x + 1) / (max_y - min_y + 1)) * (max(abs_Dx, abs_Dy) / min(abs_Dx, abs_Dy)) > flip_ave:
        # flipped PM gain projected by D-bias <-> L-bias: width / height, vs abs(xD) / height for oriented blobs?

        rdn += 1  # or += N: ratio of comp_P cost to comp_p cost?
        flip(blob, rdn)  # vertical rescan -> comp_Px_, or scan_Py_-> xd_dev_P, flip_eval(pos xd_dev_P): >> 90?

    mPP = 0, [], []  # s, PP (with S_ders), Py_ (with P_ders and e_ per P in Py)
    dPP = 0, [], []  # PP: pattern of patterns
    SmPP, SdPP, Sm_, Sd_ = [], [], [], []
    mPP_, dPP_, yP_ = [], [], []
    Py_ = blob[2]  # unless oriented?
    _P = Py_.popleft()  # initial comparand

    while Py_:  # comp_P starts from 2nd P, top-down
        P = Py_.popleft()
        _P, _ms, _ds = comp_P(norm, P, _P)  # per blob, before orient

        while Py_:  # form_PP starts from 3rd P
            P = Py_.popleft()
            P, ms, ds = comp_P(norm, P, _P)  # P: S_vars += S_ders in comp_P
            if ms == _ms:
                mPP = form_PP(1, P, mPP)
            else:
                mPP = term_PP(1, mPP)  # SPP += S, PP eval for orient, incr_comp_P, scan_par..?
                mPP_.append(mPP)
                for par, S in zip(mPP[1], SmPP):  # blob-wide summation of 16 S_vars from incr_PP
                    S += par
                    Sm_.append(S)  # or S is directly modified in SvPP?
                SmPP = Sm_  # but SPP is redundant, if len(PP_) > ave?
                mPP = ms, [], []  # s, PP, Py_ init
            if ds == _ds:
                dPP = form_PP(0, P, dPP)
            else:
                dPP = term_PP(0, dPP)
                dPP_.append(dPP)
                for var, S in zip(dPP[1], SdPP):
                    S += var
                    Sd_.append(S)
                SdPP = Sd_
                dPP = ds, [], []
            _P = P;
            _ms = ms;
            _ds = ds

    # S_ders | S_vars eval for PP ) seg ) blob orient, incr rng | der comp_P -> redun alt P ) pP) PP ) seg ) blob?
    return blob, SmPP, mPP_, SdPP, dPP_  # blob | PP_? comp_P over fork_, after comp_segment?


def comp_P(norm, P, _P):  # forms vertical derivatives of P vars, also conditional ders from DIV comp

    (s, x0, L, I, G, Dx, Dy, dert_), xd = P
    (_s, _x0, _L, _I, _G, _Dx, _Dy, _dert_), _xd = P
    xdd = 0  # optional, 2Le norm / D? s_xdd and s_dL correlate, s_dx position and s_dL dimension don't?

    mx = (x0 + L - 1) - _x0  # vx = ave_xd - xd: distance (cost) decrease vs. benefit incr? or:
    if x0 > _x0: mx -= x0 - _x0  # mx = x olp, - ave_mx -> vxP, distant P mx = -(ave_xd - xd)?

    dL = L - _L;
    mL = min(L, _L)  # relative olp = mx / L? ext_miss: Ddx + DL?
    dI = I - _I;
    mI = min(I, _I)  # L and I are dims vs. ders, not rdn | select, I per quad, no norm?
    '''
    | S: I + G + Dx + Dy: sum of lower params is a top-level param?
    '''
    if norm:  # if xD: derivatives are xd- normalized before comp:
        hyp = math.hypot(xd, 1)  # len incr = hyp / 1 (vert distance == 1)

        Dx = (Dx * hyp + Dy / hyp) / 2 / hyp  # est D over ver_L, Ders summed in ver / lat ratio
        Dy = (Dy / hyp - Dx * hyp) / 2 * hyp  # est D over lat_L
        G = math.hypot(Dy, Dx)  # reformed, not adjusted?

    dDx = Dx - _Dx;
    mDx = min(Dx, _Dx)
    dDy = Dy - _Dy;
    mDy = min(Dy, _Dy)  # lat sum of y_ders also indicates P match and orientation?
    dG = G - _G;
    mG = min(G, _G)  # or no G comp: redundant to Ds?

    Pd = xdd + dL + dI + dG + dDx + dDy  # defines dPP, dx does not correlate
    Pm = mx + mL + mI + mG + mDx + mDy  # defines mPP; comb rep value = Pm * 2 + Pd?

    if dI * dL > div_ave:  # potential d compression, vs. ave * 21(7*3)?

        # DIV comp: cross-scale d, neg if cross-sign, no ndx: single, yes nmx: summed?
        # for S: summed vars I, D, M: nS = S * rL, ~ rS,rP: L defines P?

        rL = L / _L  # L defines P, SUB comp of rL-normalized nS:
        nI = I * rL;
        ndI = nI - _I;
        nmI = min(nI, _I)  # vs. nI = dI * nrL?

        nDx = Dx * rL;
        ndDx = nDx - _Dx;
        nmDx = min(nDx, _Dx)
        nDy = Dy * rL;
        ndDy = nDy - _Dy;
        nmDy = min(nDy, _Dy)

        Pnm = mx + nmI + nmDx + nmDy  # normalized m defines norm_vPP, if rL

        if Pm > Pnm:
            nmPP_rdn = 1; mPP_rdn = 0  # added to rdn, or diff alt, olp, div rdn?
        else:
            mPP_rdn = 1; nmPP_rdn = 0

        Pnd = xdd + ndI + ndDx + ndDy  # normalized d defines norm_dPP or ndPP

        if Pd > Pnd:
            ndPP_rdn = 1; dPP_rdn = 0  # value = D | nD
        else:
            dPP_rdn = 1; ndPP_rdn = 0

        div_f = 1
        nvars = Pnm, nmI, nmDx, nmDy, mPP_rdn, nmPP_rdn, \
                Pnd, ndI, ndDx, ndDy, dPP_rdn, ndPP_rdn

    else:
        div_f = 0  # DIV comp flag
        nvars = 0  # DIV + norm derivatives

    P_ders = Pm, Pd, mx, xd, mL, dL, mI, dI, mDx, dDx, mDy, dDy, div_f, nvars

    vs = 1 if Pm > ave * 7 > 0 else 0  # comp cost = ave * 7, or rep cost: n vars per P?
    ds = 1 if Pd > 0 else 0

    return (P, P_ders), vs, ds


''' no comp_q_(q_, _q_, yP_): vert comp by ycomp, ortho P by orientation?
    comp_P is not fuzzy: x, y vars are already fuzzy?

    no DIV comp(L): match is insignificant and redundant to mS, mLPs and dLPs only?:

    if dL: nL = len(q_) // len(_q_)  # L match = min L mult
    else: nL = len(_q_) // len(q_)
    fL = len(q_) % len(_q_)  # miss = remainder 

    no comp aS: m_aS * rL cost, minor cpr / nL? no DIV S: weak nS = S // _S; fS = rS - nS  
    or aS if positive eV (not qD?) = mx + mL -ave:

    aI = I / L; dI = aI - _aI; mI = min(aI, _aI)  
    aD = D / L; dD = aD - _aD; mD = min(aD, _aD)  
    aM = M / L; dM = aM - _aM; mM = min(aM, _aM)

    d_aS comp if cs D_aS, iter dS - S -> (n, M, diff): var precision or modulo + remainder? 
    pP_ eval in +vPPs only, per rdn = alt_rdn * fork_rdn * norm_rdn, then cost of adjust for pP_rdn? '''


def form_PP(typ, P, PP):  # increments continued vPPs or dPPs (not pPs): incr_blob + P_ders?

    P, P_ders, S_ders = P
    s, ix, x, I, D, Dy, M, My, G, oG, Olp, t2_ = P
    L2, I2, D2, Dy2, M2, My2, G2, OG, Olp2, Py_ = PP

    L2 += len(t2_)
    I2 += I
    D2 += D;
    Dy2 += Dy
    M2 += M;
    My2 += My
    G2 += G
    OG += oG
    Olp2 += Olp

    Pm, Pd, mx, dx, mL, dL, mI, dI, mD, dD, mDy, dDy, mM, dM, mMy, dMy, div_f, nvars = P_ders
    _dx, Ddx, \
    PM, PD, Mx, Dx, ML, DL, MI, DI, MD, DD, MDy, DDy, MM, DM, MMy, DMy, div_f, nVars = S_ders

    Py_.appendleft((s, ix, x, I, D, Dy, M, My, G, oG, Olp, t2_, Pm, Pd, mx, dx, mL, dL, mI, dI, mD, dD, mDy, dDy, mM, dM, mMy, dMy, div_f, nvars))

    ddx = dx - _dx  # no ddxP_ or mdx: olp of dxPs?
    Ddx += abs(ddx)  # PP value of P norm | orient per indiv dx: m (ddx, dL, dS)?

    # summed per PP, then per blob, for form_pP_ or orient eval?

    PM += Pm;
    PD += Pd  # replace by zip (S_ders, P_ders)
    Mx += mx;
    Dx += dx;
    ML += mL;
    DL += dL;
    ML += mI;
    DL += dI
    MD += mD;
    DD += dD;
    MDy += mDy;
    DDy += dDy;
    MM += mM;
    DM += dM;
    MMy += mMy;
    DMy += dMy

    return s, L2, I2, D2, Dy2, M2, My2, G2, Olp2, Py_, PM, PD, Mx, Dx, ML, DL, MI, DI, MD, DD, MDy, DDy, MM, DM, MMy, DMy, nVars


def term_PP(typ, PP):  # eval for orient (as term_blob), incr_comp_P, scan_par_:

    s, L2, I2, D2, Dy2, M2, My2, G2, Olp2, Py_, PM, PD, Mx, Dx, ML, DL, MI, DI, MD, DD, MDy, DDy, MM, DM, MMy, DMy, nVars = PP

    rdn = Olp2 / L2  # rdn per PP, alt Ps (if not alt PPs) are complete?

    # if G2 * Dx > ave * 9 * rdn and len(Py_) > 2:
    # PP, norm = orient(PP) # PP norm, rescan relative to parent blob, for incr_comp, comp_PP, and:

    if G2 + PM > ave * 99 * rdn and len(Py_) > 2:
        PP = incr_range_comp_P(typ, PP)  # forming incrementally fuzzy PP

    if G2 + PD > ave * 99 * rdn and len(Py_) > 2:
        PP = incr_deriv_comp_P(typ, PP)  # forming incrementally higher-derivation PP

    if G2 + PM > ave * 99 * rdn and len(Py_) > 2:  # PM includes results of incr_comp_P
        PP = scan_params(0, PP)  # forming vpP_ and S_p_ders

    if G2 + PD > ave * 99 * rdn and len(Py_) > 2:  # PD includes results of incr_comp_P
        PP = scan_params(1, PP)  # forming dpP_ and S_p_ders

    return PP


''' incr_comp() ~ recursive_comp() in line_POC(), with Ps instead of pixels?
    with rescan: recursion per p | d (signed): frame(meta_blob | blob | PP)? '''


def incr_range_comp_P(typ, PP):
    return PP


def incr_deriv_comp_P(typ, PP):
    return PP


def scan_params(typ, PP):  # at term_network, term_blob, or term_PP: + P_ders and nvars?

    P_ = PP[11]
    Pars = [(0, 0, 0, []), (0, 0, 0, []), (0, 0, 0, []), (0, 0, 0, []), (0, 0, 0, []), (0, 0, 0, []), (0, 0, 0), []]

    for P in P_:  # repack ders into par_s by parameter type:

        s, ix, x, I, D, Dy, M, My, G, oG, Olp, t2_, Pm, Pd, mx, dx, mL, dL, mI, dI, mD, dD, mDy, dDy, mM, dM, mMy, dMy, div_f, nvars = P
        pars_ = [(x, mx, dx), (len(t2_), mL, dL), (I, mI, dI), (D, mD, dD), (Dy, mDy, dDy), (M, mM, dM), (My, mMy, dMy)]  # no nvars?

        for par, Par in zip(pars_, Pars):  # PP Par (Ip, Mp, Dp, par_) += par (p, mp, dp):

            p, mp, dp = par
            Ip, Mp, Dp, par_ = Par

            Ip += p;
            Mp += mp;
            Dp += dp;
            par_.append((p, mp, dp))
            Par = Ip, Mp, Dp, par_  # how to replace Par in Pars_?

    for Par in Pars:  # select form_par_P -> Par_vP, Par_dP: combined vs. separate: shared access and overlap eval?
        Ip, Mp, Dp, par_ = Par

        if Mp + Dp > ave * 9 * 7 * 2 * 2:  # ave PP * ave par_P rdn * rdn to PP * par_P typ rdn?
            par_vPS, par_dPS = form_par_P(0, par_)
            par_Pf = 1  # flag
        else:
            par_Pf = 0;
            par_vPS = Ip, Mp, Dp, par_;
            par_dPS = Ip, Mp, Dp, par_

        Par = par_Pf, par_vPS, par_dPS
        # how to replace Par in Pars_?

    return PP


def form_par_P(typ, param_):  # forming parameter patterns within par_:

    p, mp, dp = param_.pop()  # initial parameter
    Ip = p, Mp = mp, Dp = dp, p_ = []  # Par init

    _vps = 1 if mp > ave * 7 > 0 else 0  # comp cost = ave * 7, or rep cost: n vars per par_P?
    _dps = 1 if dp > 0 else 0

    par_vP = Ip, Mp, Dp, p_  # also sign, typ and par olp: for eval per par_PS?
    par_dP = Ip, Mp, Dp, p_
    par_vPS = 0, 0, 0, []  # IpS, MpS, DpS, par_vP_
    par_dPS = 0, 0, 0, []  # IpS, MpS, DpS, par_dP_

    for par in param_:  # all vars are summed in incr_par_P
        p, mp, dp = par
        vps = 1 if mp > ave * 7 > 0 else 0
        dps = 1 if dp > 0 else 0

        if vps == _vps:
            Ip, Mp, Dp, par_ = par_vP
            Ip += p;
            Mp += mp;
            Dp += dp;
            par_.append(par)
            par_vP = Ip, Mp, Dp, par_
        else:
            par_vP = term_par_P(0, par_vP)
            IpS, MpS, DpS, par_vP_ = par_vPS
            IpS += Ip;
            MpS += Mp;
            DpS += Dp;
            par_vP_.append(par_vP)
            par_vPS = IpS, MpS, DpS, par_vP_
            par_vP = 0, 0, 0, []

        if dps == _dps:
            Ip, Mp, Dp, par_ = par_dP
            Ip += p;
            Mp += mp;
            Dp += dp;
            par_.append(par)
            par_dP = Ip, Mp, Dp, par_
        else:
            par_dP = term_par_P(1, par_dP)
            IpS, MpS, DpS, par_dP_ = par_dPS
            IpS += Ip;
            MpS += Mp;
            DpS += Dp;
            par_dP_.append(par_dP)
            par_vPS = IpS, MpS, DpS, par_dP_
            par_dP = 0, 0, 0, []

        _vps = vps;
        _dps = dps

    return par_vPS, par_dPS  # tuples: Ip, Mp, Dp, par_P_, added to Par

    # LIDV per dx, L, I, D, M? also alt2_: fork_ alt_ concat, for rdn per PP?
    # fpP fb to define vpPs: a_mx = 2; a_mw = 2; a_mI = 256; a_mD = 128; a_mM = 128


def term_par_P(typ, par_P):  # from form_par_P: eval for orient, re_comp? or folded?
    return par_P


def scan_par_P(typ, par_P_):  # from term_PP, folded in scan_par_? pP rdn per vertical overlap?
    return par_P_


def comp_par_P(par_P, _par_P):  # with/out orient, from scan_pP_
    return par_P


def scan_PP_(PP_):  # within a blob, also within a segment?
    return PP_


def comp_PP(PP, _PP):  # compares PPs within a blob | segment, -> forking PPP_: very rare?
    return PP


def intra_blob(frame):  # evaluate blobs for orthogonal flip, incr_rng_comp, incr_der_comp, comp_P
    I, G, Dx, Dy, xD, abs_xD, Ly, blob_, dert__ = frame

    _blob_ = []
    for blob in blob_:
        _blob_.append(eval_blob(blob, dert__))
    frame[1][2] = _blob_

    return frame  # frame of 2D patterns, to be outputted to level 2


# ************ MAIN FUNCTIONS END ***************************************************************************************

# ************ PROGRAM BODY *********************************************************************************************

# Pattern filters ----------------------------------------------------------------

ave = 15  # g value that coincides with average match: gP filter
div_ave = 1023  # filter for div_comp(L) -> rL, summed vars scaling
flip_ave = 10000  # cost of form_P and deeper?
ave_rate = 0.25  # match rate: ave_match_between_ds / ave_match_between_ps, init at 1/4: I / M (~2) * I / D (~2)
dim = 2  # number of dimensions
rng = 2  # number of pixels compared to each pixel in four directions
min_coord = rng * 2 - 1  # min x and y for form_P input: ders2 from comp over rng*2 (bidirectional: before and after pixel p)
degree = 128 / math.pi  # coef to convert radian to 256 degrees
A_coef = 2
ave_L = 10

# Main ---------------------------------------------------------------------------
start_time = time()
frame = intra_blob(frame_blobs.frame_of_blobs)
end_time = time() - start_time
print(end_time)